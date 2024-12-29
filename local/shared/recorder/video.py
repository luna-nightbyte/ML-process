from queue import Queue
from threading import Event
import cv2
panic_counter = int(0)
class Video:
    def __init__(self, name: str, source: str, queue: Queue, stopEvent: Event):
        self.queue = queue
        self.stopEvent = stopEvent
        self.input_source = source
        self.type = "video"
        self.output_path = None
        self.writer = None
        self.name = name
        self.frame_num = 0
        self.fps = 15
        self.timer = 0
        self.number_of_videos = 0
        self.no_detection_frames = 0
        self.consecutive = 0
        self.false_positive_count = 0
        self.total_frames_processed = 0
    def load_to_queue(self,input_source):
        cap = cv2.VideoCapture(self.input_source)
        i = 0
        while not self.stopEvent.is_set() and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            i+=1
            self.queue.put((self.name, i, frame))
        cap.release()
        
    def start_recording(self, output_path, frame_shape):
        width, height = frame_shape
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output_path = output_path
        self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))
        if not self.writer.isOpened():
            raise Exception(f"Failed to open VideoWriter for {self.output_path}")
        self.running = True
        self.number_of_videos = (self.number_of_videos or 0) + 1

        
    def stop_recording(self):
        self.running = False
        if self.writer:
            self.writer.release()
            print(f"Recording saved: {self.output_path}")
            self.writer = None
    
    def write_frame(self, path, frame):
        if self.output_path != path:
            return self._new_recorder(path, frame)
        if self.writer:
            self.writer.write(frame)
        else:
            panic_counter = panic_counter + 1
            if panic_counter > 10:
                print("Failed to init too many times!")
                return None
            print("Writer is not initialized\nstarting recording..")
            h,w,c = frame.shape
            self.start_recording(self.output_path,(h,w))
            self.write_frame(path,frame)
            
    def _new_recorder(self,output_path, frame):
        recorder = self
        recorder.output_path = output_path
        w,h,c = frame.shape
        recorder.start_recording(output_path,(w,h))
        recorder.write_frame(self.output_path,frame)
        return recorder