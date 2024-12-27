import glob
import os
import logging as log
import contextlib
import glob
import os

import shared.vision as vision
import shared.file as files

from shared.config import settings, CSVData
import shared.target.recorder as rec




# This script reads the input folder and copies each video to the output folder.

log_file= 'detection.log'
# software variables 
log.getLogger('ultralytics').setLevel(log.WARNING)
log.basicConfig(filename=log_file, 
                level=log.INFO,  
                format='%(asctime)s\n%(message)s')

def main():
    if settings().app_name == "train" == settings().app_name:
        import apps.trainer.train as train
        train.Trianer().start(Config)
    else:
        if settings().app_name=="ai_label":
            target_folder = settings().dataset_target_folder
        else:
            target_folder = settings().output_target_folder

        input_source = files.Source().get_input_source(settings().source_folder)
        if input_source == None:
            return
        if settings().padding is not None:
            rec.process.csv_writer = CSVData(settings().csv_file_path)
            rec.process.csv_writer.open(True,["file_path","x1","y1","x2","y2","scale_x","scale_y"])
        for source in input_source:
            vision.run_object_detection(source, target_folder)
        if settings().app_name=="ai_label":
            import datasets.create_dataset
            datasets.create_dataset.Create(os.path.join(target_folder,"annotations"),settings().session_name, settings().labels)
    
    
if __name__ == "__main__":
    main()
