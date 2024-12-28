import glob
import os
import logging as log
import contextlib
import glob
import os

import shared.vision as vision
import shared.file as files

from shared.config import settings, csv_handler
import shared.recorder.process as process




# This script reads the input folder and copies each video to the output folder.

log_file= 'detection.log'
# software variables 
log.getLogger('ultralytics').setLevel(log.WARNING)
log.basicConfig(filename=log_file, 
                level=log.INFO,  
                format='%(asctime)s\n%(message)s')

def main():
    if settings.app_name == "demo":
        settings.app_name = "detection"
        main()
        settings.app_name = "ai_label"
        main()
        settings.app_name = "train"
        
    if settings.app_name == "train" == settings.app_name:
        import apps.trainer.train as train
        train.Trianer().start()
    else:
        if settings.app_name=="ai_label":
            target_folder = settings.dataset_target_folder
        else:
            target_folder = settings.output_target_folder

        input_source = files.Source().get_input_source(settings.source_folder)
        if input_source == None:
            return
        if settings.extract_detection_img:
            csv_handler.open(True)
        for source in input_source:
            print("Processing:", source)
            vision.run_object_detection(source, target_folder)
        if settings.app_name=="ai_label":
            import datasets.create_dataset
            datasets.create_dataset.Create(os.path.join(target_folder,"annotations"),settings.session_name, settings.labels)
    
    
if __name__ == "__main__":
    main()
