from queue import Queue
from threading import Event
import os
import cv2
class Image:
    def __init__(self, source: str, queue: Queue, index_queue: Queue, stopEvent: Event):
        self.queue = queue
        self.index_queue = index_queue
        self.stopEvent = stopEvent
        self.source = source
        self.type = "image"
    
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
                            self.queue.put(cv2.imread(filename=file_path))
                else:
                    self.index_queue.put(i)
                    self.queue.put(cv2.imread(filename=input_source))
                    i+=1
            loop_finished = True
        