
import cv2
class Core():
    def __init__(self):
        self.current_worker = None
        self.current_frame_num = None
        self.frame_counter = 0
        
        self.current_frame = None
        self.previous_frame = None
        
        self.current_resized_frame = None
        self.previous_resized_frame = None
        
    def update_frame(self,  frame: cv2.typing.MatLike, frame_num: int):
        self.previous_frame = self.current_frame
        self.current_frame = frame
        self.current_frame_num = frame_num
        
    def update_resized_frame(self,frame: cv2.typing.MatLike):
        self.previous_resized_frame = self.current_resized_frame
        self.current_resized_frame = frame
        
Worker = Core()