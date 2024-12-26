from queue import Queue
from threading import Event
import cv2

class Video:
    def __init__(self, source: str, queue: Queue, index_queue: Queue, stopEvent: Event):
        self.queue = queue
        self.stopEvent = stopEvent
        self.source = source
        self.type = "video"
        self.index_queue = index_queue
    def load_to_queue(self,input_source):
        cap = cv2.VideoCapture(self.source)
        i = 0
        while not self.stopEvent.is_set() and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.queue.put(frame)
            self.index_queue.put(i)
            i+=1
        cap.release()