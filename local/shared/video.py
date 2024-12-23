
import cv2
import yaml
import shared.init as ini
class Recorder:
    def __init__(self):
        self.running = False
        self.out = None
        self.cap = None
        self.frame_num = 0
        self.fps = 15
        self.timer = 0
        self.number_of_videos = 0
        self.no_detection_frames = 0
        self.consecutive = 0
        
        self.false_positive_count = 0
        self.total_frames_processed = 0

    def start_recording(self, output_path, frame_shape):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_path, fourcc, self.fps, frame_shape)
        self.running = True
        self.number_of_videos += 1
        self.no_detection_frames =0

    def stop_recording(self):
        self.running = False
        if self.out:
            self.out.release()
            self.out = None

    def write_frame(self, frame):
        if self.out:
            self.out.write(frame)
    
    def increase_frame_number(self):
        self.frame_num += 1
    def reset_frame_number(self):
        self.frame_num = 0
    def get_frame_number(self):
        return self.frame_num
    
    def increase_consecutive(self):
        self.consecutive += 1
    def reset_consecutive(self):
        self.consecutive = 0
    def get_consecutive(self):
        return self.consecutive
    
    def increase_false(self):
        self.false_positive_count += 1
    def reset_false(self):
        self.false_positive_count = 0
    def get_false(self):
        return self.false_positive_count
    
    def get_min_consecutive(self):
        return ini.Main().min_consecutive
        
    def timer_event(self):
        if self.timer>self.fps*10:
            self.timer = 0
            return True
        else:
            self.timer+=1
            return False
        
    def get_video_num(self):
        return self.number_of_videos
    
def reader(video_path, frame_queue, stop_event):

    cap = cv2.VideoCapture(video_path)
    while not stop_event.is_set() and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put(frame)
    cap.release()
    stop_event.set()



