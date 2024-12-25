
import cv2
import shared.init as init
from shared.source import image, video
import os
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
        return init.Main().min_consecutive
        
    def timer_event(self):
        if self.timer>self.fps*10:
            self.timer = 0
            return True
        else:
            self.timer+=1
            return False
        
    def get_video_num(self):
        return self.number_of_videos
    
def reader(input_source, frame_queue, stop_event):
    if os.path.exists(input_source) and not isinstance(input_source,int):
        source = image.Image(source=input_source, queue=frame_queue,stopEvent=stop_event)
    else:
        source = video.Video(source=input_source, queue=frame_queue,stopEvent=stop_event)
    source.load_to_queue(input_source=input_source)
    source.stopEvent.set()


def check_media_type(filename):
    if isinstance(filename, int):
        return "Webcam"
    # Define sets of known image and video extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}

    # Extract the file extension
    _, ext = os.path.splitext(filename)
    ext = ext.lower()  # Normalize to lowercase

    # Determine the media type
    if ext in image_extensions:
        return "Image"
    elif ext in video_extensions:
        return "Video"
    else:
        return "Unknown"