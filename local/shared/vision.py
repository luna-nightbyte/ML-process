import os
import sys
import cv2
import torch
import logging as log

from ultralytics import YOLO

import shared.recorder.process as process
from shared.config import settings
from shared.constansts import Constansts
from shared.worker import Worker

from queue import Queue
from threading import Thread, Event


# Import application trigger handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class model:
    def __init__(self):
        self.model = None
        self.useCuda = False
    def init_model(self):
        self.model = YOLO(settings.model_path)
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
        output_size = settings.output_size
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
    
    resized_frame = cv2.resize(frame, settings.output_size, interpolation=cv2.INTER_LINEAR)

    # Convert frame to tensor and send it to GPU if needed
    frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
    
    if settings.use_cuda:
        frame_tensor = frame_tensor.to('cuda')
        
    return frame_tensor
 
def check_detections(out_path: str):
    detections = []
    # Load the model
    model = Model.load_vision()
    
    # Prepare the frame tensor
    frame_tensor = get_frame_tensor(Worker.current_frame)
    frame_tensor = frame_tensor / 255.0  # Normalize to [0, 1]
    
    # Perform inference
    frame_results = model(frame_tensor)

    # Process the results
    for result in frame_results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        labels = result.boxes.cls.cpu().numpy()
        for box, conf, label in zip(boxes, confidences, labels):
            if conf > float(settings.threshold):
                trigger_label = "unknown"
                label_index = str(label).split(".")[0]
                
                # Get the corresponding label from Config
                for current_label_index, l in enumerate(settings.labels):
                    if str(current_label_index) == label_index:
                        trigger_label = l
                        break
                # Convert the bounding box coordinates to image size
                x1, y1, x2, y2 = convert_bbox_cord(box, Worker.current_frame, None)
                out_frame,err = process.save_box_if_set( (x1, y1, x2, y2), out_path)
                if err:
                    print(err)
                    out_frame = Worker.current_frame
                Worker.update_resized_frame(out_frame)
                detections.append(( (x1, y1, x2, y2), trigger_label, conf))

    return detections

def process_frame_queue(frame_queue: Queue, stop_event: Event, input_source, target_folder: str):
    
    try:
        if settings.app_name == Constansts().App().AI_LABEL:
            out_path = os.path.join(target_folder,"annotations/labelImg",settings.session_name, os.path.basename(input_source))
        else:
            out_path = os.path.join(target_folder, os.path.basename(input_source))
            
        
    except:
        out_path =  os.path.join(target_folder, f"noName_{process.MainRecorder.get_video_num()}_.mp4")
    
    while not stop_event.is_set() or not frame_queue.empty():
        if not frame_queue.empty():
            recorder_name, frame_num, frame = frame_queue.get()
            if recorder_name == Constansts().General().Sub:
                stop_event.set() # Skip looping over same frame twice when running multiple recorders.
                continue
            Worker.current_worker = recorder_name
            Worker.update_frame(frame, frame_num)
            th = None
            name = settings.app_name
            if name == Constansts().App().DETECTIN:
                from apps.post_process import trigger_handle
                th = trigger_handle
            elif name == Constansts().App().CONTINUOUS:
                from apps.continous import trigger_handle
                th = trigger_handle
            elif name == Constansts().App().AI_LABEL:
                from apps.ai_labeler import trigger_handle
                th = trigger_handle
            elif name == Constansts().App().FRAME_INSERT:
                image = process.reconstruct_original_image(input_source)
                out_path = os.path.join(target_folder,os.path.basename(input_source))
                process.MainRecorder.write_frame(out_path,image)
                print("Saved image as: ",os.path.join(target_folder,os.path.basename(input_source)))
                continue
            else:
                print("Wrong settings in docker.compose.yml... Check app name!")
                exit()
            
            detections=check_detections(out_path)
            try:
                th.handle_trigger(
                    Worker.current_frame,
                    detections,
                    out_path
                    )
            
            except Exception as e:
                print(e)
                pass
        

def run_object_detection(input_source, target_folder):
    # Initialize main frame queue and stop event
    frame_queues = [(Queue(maxsize=10), Event())]
    
    reader_threads = [Thread(target=process.MainRecorder.reader, args=(Constansts().General().Main, input_source, frame_queues[0][0], frame_queues[0][1]))]
    
    # Start the main reader thread
    reader_threads[0].start()

    if settings.extract_detection_img:
        # Initialize sub frame queue and stop event, add to lists
        sub_frame_queue = Queue(maxsize=10)
        sub_stop_event = Event()
        frame_queues.append((sub_frame_queue, sub_stop_event))
        reader_threads.append(Thread(target=process.SubRecorder.reader, args=(Constansts().General().Sub, input_source, sub_frame_queue, sub_stop_event)))

        # Start the sub-reader thread
        reader_threads[-1].start()

    try:
        # Process each frame queue
        for frame_queue, stop_event in frame_queues:
            process_frame_queue(frame_queue, stop_event, input_source, target_folder)
        
        
    finally:
        
        # Signal all stop events to gracefully terminate threads
        for _, stop_event in frame_queues:
            stop_event.set()

        process.MainRecorder.stop_recording()
        if settings.extract_detection_img:
            process.SubRecorder.stop_recording()
            
        # Join all reader threads to ensure proper cleanup
        for thread in reader_threads:
            thread.join()
