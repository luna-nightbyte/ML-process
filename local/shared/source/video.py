from queue import Queue
from threading import Event
import cv2

class Video:
    def __init__(self, source: str, queue: Queue, stopEvent: Event):
        self.queue = queue
        self.stopEvent = stopEvent
        self.source = source
        self.type = "video"
        
    def load_to_queue(self,input_source):
        cap = cv2.VideoCapture(self.source)
        while not self.stopEvent.is_set() and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.queue.put(frame)
        cap.release()