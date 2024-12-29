
import os
import yaml
import glob
import shared.server as stream

class Source:
    def __init__(self):
        self.video_url = None
        self.result = None
        self.csv_video_list = None
        try:
            self.SERVER_USER = self.get_server_user()
            self.SERVER_PASS = self.get_server_user()
        except:
            self.SERVER_USER = None
            self.SERVER_PASS = None
            
    def get_input_source(self, source_folder):
        
        if  isinstance(source_folder,int):
                self.result = [0]
        elif "input" in source_folder and not "http://" in source_folder:
                try:
                    self.result = glob.glob(os.path.join(source_folder, "*"))
                except:
                    print("No files to process..")
                    return None
        elif "http://" in source_folder:
            try: 
                video_list = stream.get_file_lists(source_folder, self.SERVER_USER, self.SERVER_PASS)
                index = 0
                for video in video_list:
                    if "http://" not in video:
                        video_list[index] = source_folder + video
                    index += 1
                    
                self.result = video_list
                        
            except:
                print("No files to process..")
                return None
        return self.result
            
    def data(self):
        return self
    
   
    def get_server_user(self):
        return self.SERVER_USER
    def get_server_pass(self):
        return self.SERVER_PASS
    def set_server_user(self,SERVER_USER):
        if SERVER_USER == "user":
            print("WARNING: Fileserving expects default username  'user'")
        self.SERVER_USER = SERVER_USER
    def set_server_pass(self,SERVER_PASS):
        if SERVER_PASS == "password":
            print("WARNING: Fileserving expects default password  'password'")
        self.SERVER_PASS = SERVER_PASS
        

def create_if_not_exist(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
def no_input_files(folder):
    return not os.path.exists(folder)
 
        
def get_labels(path):
    try:
        return yaml.safe_load(open(path, 'r'))['names']
    except FileNotFoundError:
        print(f"Missing labels file..")
        return None
            