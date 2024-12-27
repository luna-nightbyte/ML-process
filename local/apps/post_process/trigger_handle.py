
import cv2
import os
# Instantiate the recorder

import shared.target.recorder as recorder

from shared.config import settings

def handle_trigger(frame, detections, output_path: str):
    
    # Here we decide if the video contain object or not
    # if triggered:
    #     cur.execute(db.set_processed_by_user(o.observation_id, o.video_id, result_trigger))
    out_path = output_path.replace(os.path.basename(output_path),os.path.basename(output_path))
    out_e_path = output_path.replace(os.path.basename(output_path),f"E_{os.path.basename(output_path)}")
    media_type = recorder.check_media_type(output_path)
    
    bbox_rec = None
    if len(detections) > 0 and not recorder.process.running:
        height, width, _ = frame.shape
        fps = 30  # Set your desired FPS
        if  media_type == "Video" or media_type == "Webcam":
            print("Recording to",out_path)
            recorder.process.start_recording(out_path, (width, height))
            # recorder.process.start_recording(out_e_path,settings().output_size)
        elif media_type == "Image":
            print("Saving image to",out_path)
            for (box_frame, box, label, conf) in detections:
                if settings().show_bbox:
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                recorder.process.type = recorder.process.source.type
                recorder.process.write_frame(out_e_path,box_frame)
            
            cv2.imwrite(out_path, frame)
    if not len(detections) > 0:
        recorder.process.no_detection_frames += 1
    else:
        recorder.process.no_detection_frames = 0

    if recorder.process.no_detection_frames > 15:
        recorder.process.stop_recording()

    if recorder.process.running:
        obj_index = 0
        for (box_frame, box, label, conf) in detections:
            
            obj_index += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label}:{conf:.2f}', (x1, y1 - obj_index * 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        recorder.process.write_frame(out_path,frame)

    
             
