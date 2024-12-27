import os
import sys
import cv2
import torch
import logging as log

from ultralytics import YOLO

import shared.target.recorder as recorder
from shared.config import settings
from shared.file import get_labels

from queue import Queue
from threading import Thread, Event


# Import application trigger handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class model:
    def __init__(self):
        self.model = None
        self.useCuda = False
    def init_model(self):
        self.model = YOLO(settings().model_path)
        if torch.cuda.is_available():
            print(f"GPU Name: {torch.cuda.get_device_name(0)}\n")
            self.model.to('cuda')  # Move model to GPU
            self.useCuda = True
            print("Loaded to GPU!")
        else:
            print("WARNING: Loaded model to CPU. GPU is not available!")
        return self.model
    def load_vision(self):
        if self.model is None:
            print("Loading model")
            return self.init_model()
        return self.model


Model = model()

# Configure logging
log.getLogger('ultralytics').setLevel(log.ERROR)


def convert_bbox_cord(box, new_frame,output_size):
    """
    'output_size' defaults to enviroment setting if None
    """
    if output_size is None:
        output_size = settings().output_size
    height, width, _ = new_frame.shape
    
    scale_x = width / output_size[1]
    scale_y = height / output_size[0]
    
    x1, y1, x2, y2 = map(int, box)
    original_x1 = int(x1 * scale_x)
    original_y1 = int(y1 * scale_y)
    original_x2 = int(x2 * scale_x)
    original_y2 = int(y2 * scale_y)
    
    return (original_x1, original_y1, original_x2, original_y2)


def get_frame_tensor(frame):
    # Resize the frame to the desired size
    
    resized_frame = cv2.resize(frame, settings().output_size, interpolation=cv2.INTER_LINEAR)

    # Convert frame to tensor and send it to GPU if needed
    frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
    
    if settings().use_cuda:
        frame_tensor = frame_tensor.to('cuda')
        
    return frame_tensor

def check_detections(frame: cv2.typing.MatLike, out_path: str):
    detections = []
    # Load the model
    model = Model.load_vision()
    
    # Prepare the frame tensor
    frame_tensor = get_frame_tensor(frame)
    frame_tensor = frame_tensor / 255.0  # Normalize to [0, 1]
    
    # Perform inference
    frame_results = model(frame_tensor)

    # Process the results
    for result in frame_results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        labels = result.boxes.cls.cpu().numpy()
        i = 0
        for box, conf, label in zip(boxes, confidences, labels):
            if conf > float(settings().threshold):
                trigger_label = "unknown"
                label_index = str(label).split(".")[0]
                
                # Get the corresponding label from Config
                for current_label_index, l in enumerate(settings().labels):
                    if str(current_label_index) == label_index:
                        trigger_label = l
                        break

                # Convert the bounding box coordinates to image size
                x1, y1, x2, y2 = convert_bbox_cord(box, frame, None)
                out_frame = recorder.save_box_if_set(frame, (x1, y1, x2, y2), out_path, i, recorder.process.csv_writer)
                    
    
                i+=1
                
                detections.append((out_frame, (x1, y1, x2, y2), trigger_label, conf))

    return frame, detections

queue_i = 0
def process_frame_queue(frame_queue: Queue, index_queue: Queue, stop_event: Event, input_source, target_folder: str):
    global Config, queue_i
    try:
        if settings().app_name == "ai_label":
            out_path = os.path.join(target_folder,"annotations/labelImg",settings().SESSION_NAME, os.path.basename(input_source))
        else:
            out_path = os.path.join(target_folder, os.path.basename(input_source))
            
        
    except:
        out_path =  os.path.join(target_folder, f"noName_{recorder.process.get_video_num()}_.mp4")
    
    while not stop_event.is_set() or not frame_queue.empty():
        if not frame_queue.empty():
            th = None
            name = settings().app_name
            if name == "detection":
                from apps.post_process import trigger_handle
                th = trigger_handle
            elif name == "continuous":
                from apps.continous import trigger_handle
                th = trigger_handle
            elif name == "ai_label":
                from apps.ai_labeler import trigger_handle
                th = trigger_handle
            elif name == "frame_insert":
                frame = frame_queue.get()
                image = recorder.reconstruct_original_image(input_source, frame,queue_i)
                out_path = os.path.join(target_folder,os.path.basename(input_source))
                recorder.process.write_frame(out_path,image)
                print("Saved image as: ",os.path.join(target_folder,os.path.basename(input_source)))
                queue_i+=1
                continue
            else:
                print("Wrong settings in docker.compose.yml... Check app name!")
                exit()
                
                
            frame, detections=check_detections(frame_queue.get(),out_path)
            
            th.handle_trigger(
                frame,
                detections,
                out_path
                )
        
    recorder.process.stop_recording()

def run_object_detection(input_source,target_folder):
    frame_queue = Queue(maxsize=10)
    index_queue = Queue(maxsize=10)
    stop_event = Event() 
    reader_thread = Thread(target=recorder.process.reader, args=(input_source, frame_queue, index_queue, stop_event))
    
    reader_thread.start()
    
    if process_frame_queue(frame_queue, index_queue, stop_event, input_source ,target_folder):
        return
    reader_thread.join()

