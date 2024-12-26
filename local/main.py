import glob
import os
import logging as log
import contextlib
import glob
import os

import shared.vision as vision
import shared.file as files

from shared.config import settings, csv_data
from shared.target.recorder import process




# This script reads the input folder and copies each video to the output folder.
Config = settings()
log_file= 'detection.log'
# software variables 
log.getLogger('ultralytics').setLevel(log.WARNING)
log.basicConfig(filename=log_file, 
                level=log.INFO,  
                format='%(asctime)s\n%(message)s')

def main():
    if Config.APP_NAME == "train" == Config.APP_NAME:
        import apps.trainer.train as train
        train.Trianer().start(Config)
    else:
        if Config.APP_NAME=="ai_label":
            target_folder = Config.dataset_target_folder
        else:
            target_folder = Config.output_target_folder

        input_source = files.Source().get_input_source(Config.source_folder)
        if input_source == None:
            return
        process.csv_writer = csv_data(settings().csv_file_path)
        process.csv_writer.open(True,["file_path","x1","y1","x2","y2","scale_x","scale_y"])
        for source in input_source:
            vision.run_object_detection(source, target_folder)
        if Config.APP_NAME=="ai_label":
            import datasets.create_dataset
            datasets.create_dataset.Create(os.path.join(target_folder,"annotations"),Config.SESSION_NAME, Config.labels)
    
    
if __name__ == "__main__":
    main()
