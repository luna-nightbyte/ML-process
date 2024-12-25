import glob
import os
import logging as log
import contextlib
import glob
import os
import shared.vision as vision
import shared.init as init
import shared.file as files




# This script reads the input folder and copies each video to the output folder.
Config = init.Main()
log_file= 'detection.log'
# software variables 
log.getLogger('ultralytics').setLevel(log.WARNING)
log.basicConfig(filename=log_file, 
                level=log.INFO,  
                format='%(asctime)s\n%(message)s')

def main():
    if "train" == Config.APP_NAME:
        import apps.trainer.train as train
        train.Trianer().start(Config)
    else:
        if Config.APP_NAME=="ai_label":
            target_folder = Config.dataset_target_folder
        else:
            target_folder = Config.output_target_folder

        input_source = files.Source().get_input_source(Config.source_folder)
  
        for source in input_source:
            vision.run_object_detection(source, target_folder)
        if Config.APP_NAME=="ai_label":
            import datasets.create_dataset
            datasets.create_dataset.Create(os.path.join(target_folder,"annotations"),Config.SESSION_NAME, Config.labels)
    
    
if __name__ == "__main__":
    main()
