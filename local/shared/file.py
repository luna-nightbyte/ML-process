
import os
import yaml
import glob
import shared.server as stream
class Video:
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
            
    def get_video_list(self, source_folder):
        input = source_folder.lower()
        
        if  input == "0":
                self.result = [0]
        elif "input" in input and not "http://" in input:
                try:
                    self.result = glob.glob(os.path.join(source_folder, "*.mp4"))
                except:
                    print("No files to process..")
                    exit()
        elif "http://" in input:
            try: 
                video_list = stream.get_file_lists(input,self.SERVER_USER,self.SERVER_PASS)
                index = 0
                for video in video_list:
                    if "http://" not in video:
                        video_list[index] = input + video
                    index += 1
                    
                self.result = video_list
                        
            except:
                print("No files to process..")
                exit()
        return self.result
            
    def data(self):
        return self
    
   
    def get_server_user(self):
        return self.SERVER_USER
    def get_server_pass(self):
        return self.SERVER_PASS
    def get_server_url(self):
        return self.SERVER_URL
    def set_server_user(self,SERVER_USER):
        self.SERVER_USER = SERVER_USER
    def set_server_pass(self,SERVER_PASS):
        self.SERVER_PASS = SERVER_PASS
        

def create_if_not_exist(folder):
    if not os.path.exists(folder):
        print("mkdir",folder)
        os.makedirs(folder)
        
def no_input_files(folder):
    return not os.path.exists(folder)
 
        
def get_labels(path):
    try:
        return yaml.safe_load(open(path, 'r'))['names']
    except FileNotFoundError:
        print(f"Missing labels file..")
        return None
            