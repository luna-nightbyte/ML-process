import os

import shared.file as files
class settings:
    
    def __init__(self):
        # Extracting the arguments
        self.model_path = os.path.join("data",os.getenv('MODEL_PATH'))
        self.threshold = os.getenv('THRESHOLD')
        self.OUTPUT_SIZE: tuple
        self.PADDING = ""
        output_size_enviroment = os.getenv('OUTPUT_SIZE')
        self.show_bbox = os.getenv('SHOW_BOUNDING_BOX')
        if self.show_bbox == "":
            self.show_bbox  = None
        else:
            if self.show_bbox.lower() == "true":
                self.show_bbox = True
            else:
                self.show_bbox = False
        if output_size_enviroment != "":
            size = output_size_enviroment.split(",")
            try:
                self.OUTPUT_SIZE = (int(size[0]),int(size[1]))
                self.PADDING = os.getenv('PADDING')
            except:
                print("Wrong frame dimentions!")
                exit()
        try: 
            self.source_folder = int(os.getenv('INPUT_DIR'))
        except:
            self.source_folder =  os.path.join("./data/", os.getenv('INPUT_DIR'))
            
        self.dataset_target_folder = os.path.join("./datasets")
        self.output_target_folder =os.path.join("./data/output/" , os.getenv('SESSION_NAME'))
        self.min_consecutive = os.getenv('CONSECUTIVE')
        self.APP_NAME = os.getenv('APP_NAME')
        self.SESSION_NAME = os.getenv('SESSION_NAME')
        self.DATASET_YAML = "./dataset.yaml"
        self.epochs = int(os.getenv('EPOCHS'))
        self.batch = int(os.getenv('BATCH'))
        
        files.Source().set_server_user(os.getenv('SERVER_USER'))
        files.Source().set_server_pass(os.getenv('SERVER_PASS'))
        
        
        self.model = None
        self.useCuda = False
        if files.no_input_files(self.source_folder) and os.getenv('INPUT_DIR') != "0":
            print(f"No video files in '{self.source_folder}'..")
            exit()
        

        self.labels = files.get_labels("dataset.yaml")
        if self.labels is None:
            print("Missing labels file ./dataset.yaml..")
        files.create_if_not_exist(self.dataset_target_folder)
        files.create_if_not_exist(self.output_target_folder)
        files.create_if_not_exist(self.model_path)
       
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
    def draw_bbox(self):
        return self.show_bbox == True
    
    def AppName(self):
        return self.APP_NAME
    