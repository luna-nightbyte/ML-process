class Constansts:
    class App:
        def __init__(self):
            self.DEMO = "demo"
            self.AI_LABEL = "ai_label"
            self.DETECTIN = "detection"
            self.CONTINUOUS = "continuous"
            self.FRAME_INSERT = "frame_insert"
            self.TRAIN = "train"
    class General:
        def __init__(self):
            self.image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
            self.video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
            self.Image = "Image"
            self.Video = "Video"
            self.Unknown = "Unknown"
            self.Webcam = "Webcam"
            self.Sub = "Sub"
            self.Main = "Main"
            self.workDir = "/usr/src/app"
            self.extracted_file_str = "_E_"
    class CSV:
        def __init__(self):
            self.ORIGINAL_FILEPATH = "original_filepath"
            self.FRAME_NUBMER = "frame_number"
            self.DETECTION_NUMBER = "detection_number"
            self.X1 = "x1"
            self.Y1 = "y1"
            self.X2 = "x2"
            self.Y2 = "y2"
    
    class ENV:
        def __init__(self):
            self.MODEL_PATH: str = "MODEL_PATH"
            self.CSV_FILE_PATH = "CSV_FILE_PATH"
            self.SESSION_NAME = "SESSION_NAME"
            self.APP_NAME = "APP_NAME"
            self.INPUT_DIR = "INPUT_DIR"
            self.EPOCHS = "EPOCHS"
            self.BATCH = "BATCH"
            self.MODEL_IMG_SIZE = "MODEL_IMG_SIZE"
            self.CONSECUTIVE = "CONSECUTIVE"
            self.THRESHOLD = "THRESHOLD"
            self.OUTPUT_SIZE = "OUTPUT_SIZE"
            self.PADDING = "PADDING"
            self.EXTRACT_BOX = "EXTRACT_BOX"
            self.SHOW_BOUNDING_BOX = "SHOW_BOUNDING_BOX"
            self.SERVER_USER = "SERVER_USER"
            self.SERVER_PASS = "SERVER_PASS"
    
            
            