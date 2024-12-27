
import cv2
import os
import numpy as np
import pandas as pd

from cv2.typing import MatLike

from shared.source import image, video
from shared.config import settings,CSVData

class recorder:
    def __init__(self):
        self.running = False
        self.type = None
        self.cap = None
        self.source = None
        self.frame_num = 0
        self.fps = 15
        self.timer = 0
        self.number_of_videos = 0
        self.no_detection_frames = 0
        self.consecutive = 0
        self.csv_writer: CSVData = None
        
        self.false_positive_count = 0
        self.total_frames_processed = 0
        
    def start_recording(self, output_path, frame_shape):
        if self.running:
            return
        
        self._init()
        self.running = True
        if self.type == "video":
            video_path = output_path
            # video_path = output_path.replace(os.path.splitext(output_path)[1],f"_Extracted_{os.path.splitext(output_path)[1]}") 
            self.source.start_recording(video_path,frame_shape)
        else:
            return
        
            
        

    def stop_recording(self):
        self.source.stop_recording()

    def write_frame(self,path, frame):
        """Path is only needed for single images."""
        if self.type is None:
            print("recorder not running!")
            return
        return self.source.write_frame(path, frame)
    
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
        return settings().min_consecutive
        
    def timer_event(self):
        if self.timer>self.fps*10:
            self.timer = 0
            return True
        else:
            self.timer+=1
            return False
        
    def get_video_num(self):
        return self.number_of_videos
    
    def reader(self,input_source, frame_queue, index_queue, stop_event):
        if os.path.exists(input_source) and not isinstance(input_source,int):
            if ".mp4" in input_source:
                cv2.VideoCapture(input_source)
                self.source = video.Video(source=input_source, queue=frame_queue, stopEvent=stop_event)
            else:
                self.source = image.Image(source=input_source, queue=frame_queue, stopEvent=stop_event)
            print(self.source.type)    
        elif isinstance(input_source,int):
            cv2.VideoCapture(input_source)
            self.source = video.Video(source=input_source, queue=frame_queue, stopEvent=stop_event)  
        else:
            print("no valid input")
        self.source.load_to_queue(input_source=input_source)
        self.source.stopEvent.set()
        
    def _init(self):
        self.stopEvent = self.source.stopEvent
        self.type = self.source.type
        self.index_queue = self.source
        self.output_path = self.source.output_path
        self.writer = self.source.writer
        self.frame_num = self.source.frame_num
        self.fps = self.source.fps
        self.timer = self.source.timer
        self.number_of_videos = self.source.number_of_videos
        self.no_detection_frames = self.source.no_detection_frames
        self.consecutive = self.source.consecutive
        self.false_positive_count = self.source.false_positive_count
        self.total_frames_processed = self.source.total_frames_processed
    

process = recorder()


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


def reconstruct_original_image(input_source: str, resized_image: np.ndarray, index_queue: int):
    csv_file = CSVData(settings().csv_file_path)
    
    data = csv_file.read()
    input_file_identifier = os.path.basename(input_source).split("_det")[0]
    original_file_path = None
    
    for line in data:
        if original_file_path is not None:
            break
        for key in line.keys():
            if key == "file_path":
                file_path = line.get(key)
                if input_file_identifier in file_path:
                    original_file_path = line.get(key)
                    x1, y1, x2, y2 = line.get("x1"), line.get("y1"), line.get("x2"), line.get("y2")
                    scale_x, scale_y =line.get("scale_x"), line.get("scale_y")
                    break
      
    original_frame = cv2.imread(original_file_path)
    frame_width, frame_height = original_frame.shape[0],original_frame.shape[1]
    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
    frame_width, frame_height = int(frame_width), int(frame_height)

    
    original_width = x2 - x1
    original_height = y2 - y1

    if original_width <= 0 or original_height <= 0:
        raise ValueError("Invalid bounding box dimensions.")

    
    reconstructed_region = cv2.resize(
        resized_image,
        (original_width, original_height),
        interpolation=cv2.INTER_LINEAR
    )

    
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(frame_width, x1 + original_width)
    y2 = min(frame_height, y1 + original_height)
    
    
    region_width = x2 - x1
    region_height = y2 - y1
    
    x1 = max(0, x1)
    y1 = max(0, y1)
    region_width = max(0, min(region_width, original_frame.shape[1] - x1))
    region_height = max(0, min(region_height, original_frame.shape[0] - y1))
    print(f"x1: {x1}, y1: {y1}, region_width: {region_width}, region_height: {region_height}")
    print(f"original_frame shape: {original_frame.shape}")
    print(f"reconstructed_region shape: {reconstructed_region.shape}")


    # Crop the reconstructed region if it overflows the clamped box
    reconstructed_region = reconstructed_region[:region_height, :region_width]

    # Place the reconstructed region in the original frame
    original_frame[y1:y1 + region_height, x1:x1 + region_width] = reconstructed_region

    return original_frame


def extract_and_resize(input_source_path: str, frame: np.ndarray, bbox, output_size, csv_file: CSVData):
    """
    Extracts a detected region from the frame, resizes it, and adjusts the extracted box to include
    the missing parts when scaling down, avoiding black padding.

    Args:
        frame (np.ndarray): The input image.
        bbox (tuple): The bounding box (x1, y1, x2, y2) in pixel coordinates.
        output_size (tuple): The desired output size (width, height).

    Returns:
        np.ndarray: The resized image without black padding.
        tuple: The scaling factors (scale_x, scale_y).
    """
    if output_size is None:
        output_size = settings().output_size

    x1, y1, x2, y2 = bbox
    ih, iw, _ = frame.shape
    
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(iw, x2), min(ih, y2)

    
    cropped_img = frame[y1:y2, x1:x2]

    
    crop_width = x2 - x1
    crop_height = y2 - y1

    if crop_width == 0 or crop_height == 0:
        raise ValueError("Bounding box dimensions are invalid or outside the image boundaries.")

    
    scale_x = output_size[0] / crop_width
    scale_y = output_size[1] / crop_height
    
    
    scale_factor = min(scale_x, scale_y)  # Maintain aspect ratio

    if scale_factor < 1.0:
        
        new_crop_width = int(output_size[0] / scale_factor)
        new_crop_height = int(output_size[1] / scale_factor)
        
        x1 = max(0, x1 - (new_crop_width - crop_width) // 2)
        y1 = max(0, y1 - (new_crop_height - crop_height) // 2)
        x2 = min(iw, x1 + new_crop_width)
        y2 = min(ih, y1 + new_crop_height)

        
        cropped_img = frame[y1:y2, x1:x2]
    
    csv_file.write({
        "file_path": input_source_path.replace("./","/usr/src/app/", 1),
        "x1": x1, 
        "y1": y1,
        "x2": x2, 
        "y2": y2, 
        "scale_x": scale_x, 
        "scale_y": scale_y
        }
    )
    
    
    final_resized_img = cv2.resize(cropped_img, output_size, interpolation=cv2.INTER_LINEAR)

    return final_resized_img

import shared.config as config

def save_box_if_set(frame, box, output_path: str, i: int, csv_file: CSVData):
    if config.settings().padding != "":
        extracted_image_path = output_path.replace(f"{os.path.splitext(output_path)[1]}",f"_det-{i}{os.path.splitext(output_path)[1]}")
        dir = os.path.dirname(os.path.abspath(extracted_image_path))
        out_dir = os.path.join(dir,"detections")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        output_path_corrected_path = os.path.join(os.path.dirname(os.path.abspath(output_path)),f"{os.path.splitext(os.path.basename(output_path))[0]}_{process.get_video_num()}{os.path.splitext(os.path.basename(output_path))[1]}")
        
        extracted_image_path = os.path.join(out_dir, os.path.basename(extracted_image_path))
        
        output_size = settings().output_size
        output_frame = extract_and_resize(output_path_corrected_path, frame, box, output_size,csv_file)
        return output_frame
        
    if config.settings().show_bbox:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)