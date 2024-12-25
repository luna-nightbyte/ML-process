import os
import sys
import cv2
import torch
import logging as log

from queue import Queue
from threading import Thread, Event

# local

import shared.recorder as recorder
import shared.init as init

# Import application trigger handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



Config = init.Main()

Recorder = recorder.Recorder()
# Configure logging
log.getLogger('ultralytics').setLevel(log.ERROR)


def convert_bbox_cord(box, new_frame,old_frame_size=(640,640)):

    height, width, _ = new_frame.shape
    
    scale_x = width / old_frame_size[1]
    scale_y = height / old_frame_size[0]
    
    x1, y1, x2, y2 = map(int, box)
    original_x1 = int(x1 * scale_x)
    original_y1 = int(y1 * scale_y)
    original_x2 = int(x2 * scale_x)
    original_y2 = int(y2 * scale_y)
    
    return (original_x1, original_y1, original_x2, original_y2)

                   
def get_frame_tensor(frame, size=(640,640),cuda=False):
    resized_frame = cv2.resize(frame, size, interpolation=cv2.INTER_LINEAR)
    if cuda:
        frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float().to('cuda')
    
    else:
        frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
    return  frame_tensor

from cv2.typing import MatLike
def check_detections(model_path: str, frame: MatLike, threshold: str, size: tuple=(640,640)):
    global Recorder
    # Returns
    trigger_bool = False
    detections = []
    model = Config.load_vision()
    frame_tensor = get_frame_tensor(frame, size,Config.useCuda)
    frame_tensor = frame_tensor / 255.0
    frame_results = model(frame_tensor)
    
    for result in frame_results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        labels = result.boxes.cls.cpu().numpy()
        for box, conf, label in zip(boxes, confidences, labels):

            m = init.Main()
            if conf > float(threshold):
                labels=m.get_labels()
                trigger_label = "unknown"
                label_index = str(label).split(".")[0]
                current_label_index = 0
                for l in labels:
                    if str(current_label_index) == label_index:
                        trigger_label = l 
                        break
                    current_label_index += 1
                
                x1, y1, x2, y2 = convert_bbox_cord(box,frame,size)
               # x1, y1, x2, y2 = map(int, out_box)
                # trigger_label = label
                detections.append(((x1, y1, x2, y2), trigger_label, conf))
                trigger_bool = True
    
    return frame,trigger_bool, detections

def process_frame_queue(frame_queue: Queue, stop_event: Event, video_path, recorder, target_folder: str):
    global Config
    try:
        if Config.APP_NAME == "ai_label":
            out_path = os.path.join(target_folder,"annotations/labelImg",Config.SESSION_NAME, os.path.basename(video_path))
        else:
            out_path = os.path.join(target_folder, os.path.basename(video_path))
        
    except:
        out_path =  os.path.join(target_folder, f"noName_{Recorder.get_video_num()}_.mp4")

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
            frame,trigger_bool, detections=check_detections(Config.model_path, frame_queue.get(), Config.threshold,(640,640))
            th.handle_trigger(
                frame,
                trigger_bool,
                detections,
                out_path,
                recorder
                )
        
    recorder.stop_recording()

def run_object_detection(input_source,target_folder):
    global Recorder
    frame_queue = Queue(maxsize=10)
    stop_event = Event() 
    reader_thread = Thread(target=recorder.reader, args=(input_source, frame_queue, stop_event))
    
    reader_thread.start()
    if process_frame_queue(frame_queue, stop_event, input_source, Recorder ,target_folder):
        return
    reader_thread.join()
    


