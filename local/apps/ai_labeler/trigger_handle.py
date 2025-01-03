
import os
import time
import random
from shared.recorder.process import MainRecorder
import shared.annotate as annotate
import shared.file as files
skip = 0
def handle_trigger(frame,detections,output_path: str):
    global skip
    MainRecorder.increase_frame_number()
    files.create_if_not_exist(os.path.dirname(output_path))
    if len(detections) > 0:
        MainRecorder.increase_consecutive()
        if int(MainRecorder.get_consecutive()) >= int(MainRecorder.get_min_consecutive()):  
            if skip > 5:
                skip = 0
                timestamp= int(time.time())
                name = os.path.splitext(os.path.basename(output_path))[0]
                img_name = f"{name}-{timestamp}-{MainRecorder.get_frame_number()}.jpg"
                tmp=output_path.split("/")
                tmp=tmp[len(tmp)-1]
                full_output_path=output_path.replace(tmp,img_name)
                # frame = rec.resize_for_tensor(frame, size=(640, 640))
                for (bbox, label, conf) in detections:
                    
                    annotate.save(img_name, frame, bbox, label, full_output_path) 
            else:
                skip += 1      
    else:
        MainRecorder.reset_consecutive()
        # Handle false positives
        MainRecorder.increase_false()
        
        # Calculate if this false positive should be saved
        if random.random() < 0.1:  # 10% chance
            timestamp = int(time.time())
            name = os.path.splitext(os.path.basename(output_path))[0]

            img_name = f"{name}-{timestamp}-{MainRecorder.get_frame_number()}.jpg"
            
            tmp = output_path.split("/")
            tmp = tmp[len(tmp)-1]
            full_output_path = output_path.replace(tmp, img_name)
            # Save the false positive frame
            annotate.save(img_name, frame, None, 'false_positive', full_output_path)
    
    return None
    
         