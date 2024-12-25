import shared.recorder as rec
import cv2
import os
# Instantiate the recorder
recorder = rec.Recorder()

def handle_trigger(frame,triggered, detections, output_path,r):
    
    # Here we decide if the video contain object or not
    # if triggered:
    #     cur.execute(db.set_processed_by_user(o.observation_id, o.video_id, result_trigger))
    global recorder
    out_path = output_path.replace(os.path.basename(output_path),os.path.basename(output_path).replace(".",f"_{recorder.get_video_num()}."))
    media_type = rec.check_media_type(output_path)
    if triggered and not recorder.running:
        height, width, _ = frame.shape
        fps = 30  # Set your desired FPS
        if  media_type == "Video" or media_type == "Webcam":
            print("Recording to",out_path)
            recorder.start_recording(out_path, (width, height))
        elif media_type == "Image":
            print("Saving image to",out_path)
            cv2.imwrite(out_path, frame)
    if not triggered:
        recorder.no_detection_frames += 1
    else:
        recorder.no_detection_frames = 0

    if recorder.no_detection_frames > 15:
        recorder.stop_recording()

    if recorder.running:
        obj_index = 0
        for (box, label, conf) in detections:
            obj_index += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label}:{conf:.2f}', (x1, y1 - obj_index * 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        recorder.write_frame(frame)

    
             
