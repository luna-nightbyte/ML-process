import os
import sys
import cv2
import torch
import logging as log

from ultralytics import YOLO

import shared.target.recorder as recorder
import shared.config as config

from queue import Queue
from threading import Thread, Event

# Import application trigger handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Config = config.settings()

class model:
    def __init__(self):
        self.model = None
        self.useCuda = False
    def init_model(self):
        self.model = YOLO(Config.model_path)
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
        output_size = Config.OUTPUT_SIZE
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
    
    resized_frame = cv2.resize(frame, Config.OUTPUT_SIZE, interpolation=cv2.INTER_LINEAR)

    # Convert frame to tensor and send it to GPU if needed
    frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
    
    if Config.useCuda:
        frame_tensor = frame_tensor.to('cuda')
        
    return frame_tensor

def check_detections( frame: cv2.typing.MatLike):
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
        
        for box, conf, label in zip(boxes, confidences, labels):
            if conf > float(Config.threshold):
                trigger_label = "unknown"
                label_index = str(label).split(".")[0]
                
                # Get the corresponding label from Config
                for current_label_index, l in enumerate(Config.get_labels()):
                    if str(current_label_index) == label_index:
                        trigger_label = l
                        break

                # Convert the bounding box coordinates to image size
                x1, y1, x2, y2 = convert_bbox_cord(box, frame, None)

                # Extract and resize the detected region
                # Optionally draw the bounding box on the frame

                detections.append(( (x1, y1, x2, y2), trigger_label, conf))

    return frame, detections


def process_frame_queue(frame_queue: Queue, stop_event: Event, video_path, target_folder: str):
    global Config
    try:
        if Config.APP_NAME == "ai_label":
            out_path = os.path.join(target_folder,"annotations/labelImg",Config.SESSION_NAME, os.path.basename(video_path))
        else:
            out_path = os.path.join(target_folder, os.path.basename(video_path))
        
    except:
        out_path =  os.path.join(target_folder, f"noName_{recorder.process.get_video_num()}_.mp4")

    while not stop_event.is_set() or not frame_queue.empty():
        if not frame_queue.empty():
            th = None
            name = Config.AppName()
            if name == "detection":
                from apps.post_process import trigger_handle
                th = trigger_handle
            elif name == "continuous":
                from apps.continous import trigger_handle
                th = trigger_handle
            elif name == "ai_label":
                from apps.ai_labeler import trigger_handle
                th = trigger_handle
            else:
                print("Wrong settings in docker.compose.yml... Check app name!")
                exit()
            frame, detections=check_detections(frame_queue.get())
            
            th.handle_trigger(
                frame,
                detections,
                out_path
                )
        
    recorder.process.stop_recording()

def run_object_detection(input_source,target_folder):
    frame_queue = Queue(maxsize=10)
    stop_event = Event() 
    reader_thread = Thread(target=recorder.process.reader, args=(input_source, frame_queue, stop_event))
    
    reader_thread.start()
    if process_frame_queue(frame_queue, stop_event, input_source ,target_folder):
        return
    reader_thread.join()

