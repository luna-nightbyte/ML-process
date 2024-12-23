import torch
import os
import shared.file as files

from ultralytics import YOLO

class Main:
    def __init__(self):
        # Extracting the arguments
        self.model_path = os.path.join("data",os.getenv('MODEL_PATH'))
        self.threshold = os.getenv('THRESHOLD')
        self.source_folder =  os.path.join("./data/", os.getenv('INPUT_DIR'))
        
        self.dataset_target_folder = os.path.join("./datasets")
        self.output_target_folder =os.path.join("./data/output/" , os.getenv('SESSION_NAME'))
        self.min_consecutive = os.getenv('CONSECUTIVE')
        self.APP_NAME = os.getenv('APP_NAME')
        self.SESSION_NAME = os.getenv('SESSION_NAME')
        self.DATASET_YAML = "./dataset.yaml"
        self.epochs = int(os.getenv('EPOCHS'))
        self.batch = int(os.getenv('BATCH'))
        
        files.Video().set_server_user(os.getenv('SERVER_USER'))
        files.Video().set_server_pass(os.getenv('SERVER_PASS'))
        
        
        self.model = None
        self.useCuda = False
        if files.no_input_files(self.source_folder) and self.source_folder != "0":
            print(f"No video files in '{self.source_folder}'..")
            exit()
        

        self.labels = files.get_labels("dataset.yaml")
        if self.labels is None:
            print("Missing labels file ./dataset.yaml..")
        files.create_if_not_exist(self.dataset_target_folder)
        files.create_if_not_exist(self.output_target_folder)
        files.create_if_not_exist(self.model_path)
       
    def init_model(self):
        self.model = YOLO(self.model_path)
        if torch.cuda.is_available():
            print(f"GPU Name: {torch.cuda.get_device_name(0)}\n")
            self.model.to('cuda')  # Move model to GPU
            self.useCuda = True
            print("Loaded to GPU!")
        else:
            print("WARNING: Loaded model to CPU. GPU is not available!")
    def get_model(self):
        if self.model is None:
            self.init_model()
        return self.model
            
    def get_model_path(self):
        return self.model_path
    def get_threshold(self):
        return self.threshold
    def get_source_folder(self):
        return self.source_folder
    def get_target_folder(self):
        return self.target_folder
    def set_source_folder(self,folder):
        self.source_folder = folder
    def set_target_folder(self,folder):
        self.target_folder = folder
    def get_min_consecutive(self):
        return self.min_consecutive
    def get_labels(self):
        return self.labels
    
    def AppName(self):
        return self.APP_NAME
    
