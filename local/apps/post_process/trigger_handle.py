
import cv2
import os
# Instantiate the recorder

import shared.recorder.process as process

from shared.config import settings
from shared.worker import Worker

def handle_trigger(frame, detections, output_path: str):
    
    # Here we decide if the video contain object or not
    # if triggered:
    #     cur.execute(db.set_processed_by_user(o.observation_id, o.video_id, result_trigger))
    out_path = output_path.replace(os.path.basename(output_path),os.path.basename(output_path))
    out_e_path = output_path.replace(os.path.basename(output_path),f"E_{os.path.basename(output_path)}")
    media_type = process.MainRecorder.check_media_type(output_path)
    
    bbox_rec = None
    if len(detections) > 0 and not process.MainRecorder.running:
        height, width, _ = frame.shape
        fps = 30  # Set your desired FPS
        if  media_type == "Video" or media_type == "Webcam":
            process.MainRecorder.start_recording(out_path, (width, height))
            if settings.extract_detection_img: 
                process.SubRecorder.start_recording(out_e_path,settings.output_size)
        elif media_type == "Image":
            print("Saving image to",out_path)
            for (box, label, conf) in detections:
                if settings.extract_detection_img:
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                process.MainRecorder.type = process.MainRecorder.source.type
                process.MainRecorder.write_frame(out_path,frame)
                if settings.extract_detection_img:
                    process.SubRecorder.type = process.SubRecorder.source.type
                    process.SubRecorder.write_frame(out_e_path, Worker.current_resized_frame)
            # cv2.imwrite(out_path, frame)
    if not len(detections) > 0:
        process.MainRecorder.no_detection_frames += 1
    else:
        process.MainRecorder.no_detection_frames = 0

    if process.MainRecorder.no_detection_frames > 15:
        process.MainRecorder.stop_recording()
        process.SubRecorder.stop_recording()

    if process.MainRecorder.running:
        obj_index = 0
        for (box, label, conf) in detections:
            obj_index += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label}:{conf:.2f}', (x1, y1 - obj_index * 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            if settings.extract_detection_img:
                process.SubRecorder.write_frame(out_e_path, Worker.current_resized_frame)
        process.MainRecorder.write_frame(out_path,frame)
        

    
             
