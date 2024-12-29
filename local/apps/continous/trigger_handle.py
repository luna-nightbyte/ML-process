import cv2

import shared.target.recorder as recorder
# Instantiate the recorder'
def handle_trigger(frame,detections,output_path: str):

    #if recorder.timer_event():
    #    recorder.stop_recording()
    if not recorder.process.running: 
        height, width, _ = frame.shape
        recorder.process.start_recording(output_path.replace(".mp4",f"_{recorder.process.get_video_num()}.mp4"), (width, height))

    if recorder.process.running:
        obj_index = 0
        for (box, label, conf) in detections:
            obj_index += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label}:{conf:.2f}', (x1, y1 - obj_index * 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        recorder.process.write_frame(frame)