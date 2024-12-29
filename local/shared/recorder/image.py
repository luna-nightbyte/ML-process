from queue import Queue
from threading import Event
import os
import cv2
from shared.constansts import Constansts
class Image:
    def __init__(self, name: str,  source: str, queue: Queue, stopEvent: Event):
        self.queue = queue
        self.stopEvent = stopEvent
        self.source = source
        self.type = Constansts().General().Image
        self.name = name
        self.output_path = None
        self.writer = None
        self.frame_num = 0
        self.fps = 15
        self.timer = 0
        self.number_of_videos = 0
        self.no_detection_frames = 0
        self.consecutive = 0
        self.false_positive_count = 0
        self.total_frames_processed = 0
        
    
    def load_to_queue(self,input_source):
        loop_finished = False
        i = 0
        while not self.stopEvent.is_set() and not loop_finished:
            if os.path.exists(input_source):
                if os.path.isdir(input_source):
                    files = os.listdir(input_source)
                    for file in files:
                        file_path = os.path.join(input_source,file)
                        if os.path.isdir(file_path):
                            self.load_to_queue(file_path)
                        else:
                            self.queue.put((self.name, i, cv2.imread(filename=file_path)))
                else:
                    i+=1
                    self.queue.put((self.name, i, cv2.imread(filename=input_source)))
            loop_finished = True
    
    def start_recording(self, output_path, frame_shape):
        return None
    def stop_recording(self):
        return None
    def write_frame(self, path,frame):
        return cv2.imwrite(path,frame)