
import cv2

from shared.source import image, video
from shared.config import settings

import os
class recorder:
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
    
    def reader(self,input_source, frame_queue, stop_event):
        if os.path.exists(input_source) and not isinstance(input_source,int):
            source = image.Image(source=input_source, queue=frame_queue,stopEvent=stop_event)
        else:
            source = video.Video(source=input_source, queue=frame_queue,stopEvent=stop_event)
        source.load_to_queue(input_source=input_source)
        source.stopEvent.set()


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


import numpy as np
import cv2
import torch
from cv2.typing import MatLike

import cv2
import numpy as np
import cv2
import numpy as np
def extract_and_resize(frame: np.ndarray, bbox, output_size):
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
        output_size = settings().OUTPUT_SIZE

    x1, y1, x2, y2 = bbox
    ih, iw, _ = frame.shape

    # Ensure the bounding box is within the image boundaries
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(iw, x2), min(ih, y2)

    # Extract the region based on the bounding box
    cropped_img = frame[y1:y2, x1:x2]

    # If the crop size is already smaller than output size, adjust the box
    crop_width = x2 - x1
    crop_height = y2 - y1

    if crop_width == 0 or crop_height == 0:
        raise ValueError("Bounding box dimensions are invalid or outside the image boundaries.")

    # Calculate scaling factors for the crop and target output size
    scale_x = output_size[0] / crop_width
    scale_y = output_size[1] / crop_height
    scale_factor = min(scale_x, scale_y)  # Maintain aspect ratio

    if scale_factor < 1.0:
        # Scaling down: expand the crop area to fit the output size
        new_crop_width = int(output_size[0] / scale_factor)
        new_crop_height = int(output_size[1] / scale_factor)

        # Adjust the bounding box to include more content
        x1 = max(0, x1 - (new_crop_width - crop_width) // 2)
        y1 = max(0, y1 - (new_crop_height - crop_height) // 2)
        x2 = min(iw, x1 + new_crop_width)
        y2 = min(ih, y1 + new_crop_height)

        # Re-crop with the adjusted bounding box
        cropped_img = frame[y1:y2, x1:x2]

    # Resize the final cropped image to the target output size
    final_resized_img = cv2.resize(cropped_img, output_size, interpolation=cv2.INTER_LINEAR)

    return final_resized_img, (scale_x, scale_y)


def save_extracted_box(frame, box, extracted_image_path):
    """
    Extracts and saves a resized bounding box image to the specified path.

    Args:
        frame (np.ndarray): The input image.
        box (tuple): The bounding box (x1, y1, x2, y2) in pixel coordinates.
        extracted_image_path (str): Path to save the extracted image.
    """
    output_size = settings().OUTPUT_SIZE
    output_frame, scale_factor = extract_and_resize(frame, box, output_size)
    cv2.imwrite(extracted_image_path, output_frame)
