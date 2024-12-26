import os
import csv

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
        self.csv_file_path = os.path.join("/usr/src/app/data",os.getenv('CSV_FILE_PATH'))
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
    


class csv_data:
    def __init__(self,path):
        self.path = path
        self.file = None
        self.writer = None
        self.fieldnames = None
        
    def open(self, is_new_file: bool, fieldnames): 
        if self.is_open():
            return f"{self.path} already open" 
        try:
            self.file = open(self.path, mode="a", newline="")
            self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
            if is_new_file:
                self.writer.writeheader()
                self.fieldnames = fieldnames
        except Exception as e:
            self.path = None
            print(e)
            pass
        
        
        return None
    def close(self):  
        if self.file is not None:
            self.close()
            self.file = None  
            self.writer = None
        else:
            return f"{self.path} not open"
        return None
    def is_open(self):  
        return self.writer is not None
    
    def read(self):  
        output_data = [{}]
        with open(self.path, mode ='r') as file:
            reader = csv.reader(file,delimiter=' ', quotechar='|')
            output_data.clear()
            for lines in reader:
                if is_valid_input(lines):
                    data = {
                        "file_path": lines[0].split(",")[0],
                        "x1": lines[0].split(",")[1],
                        "y1": lines[0].split(",")[2],
                        "x2": lines[0].split(",")[3],
                        "y2": lines[0].split(",")[4],
                        "scale_x": lines[0].split(",")[5],
                        "scale_x": lines[0].split(",")[6]
                    }
                    output_data.append(data)
        return output_data
    def write(self,data):
        if self.path is None:
            return f"writer not properly initialyzed!"
        if self.is_open():
            # writer = csv.writer(self.file)
            self.writer.writerow(data)
            return f"wrote to file"
        else:
            err= self.open(False,self.fieldnames)
            if err is not None: 
                print(err)
                return err
            self.writer.writerow(data)
            return None

def is_valid_input(lines):
    try:
        is_at_max = lines[0].split(",")[6]
        x1 = int(lines[0].split(",")[1])
        y1 = int(lines[0].split(",")[2])
        x2 = int(lines[0].split(",")[3])
        y2 = int(lines[0].split(",")[4])
        x = x1 + x2 + y1 + y2
        return True
    except:
        return False