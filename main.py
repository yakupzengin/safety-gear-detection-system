import YOLOModel
import VideoProcessor
import DetectionDrawer
import cv2
import time
from datetime import datetime

class DetectionState:
    def __init__(self):
        self.insan_last_detected = 0
        self.baret_last_detected = 0
        self.emniyet_kemeri_last_detected = 0
        self.el_last_detected = 0
        self.eldiven_last_detected = 0
        self.yanlis_eldiven_last_detected = 0

    def reset(self):
        self.insan_last_detected = 0
        self.baret_last_detected = 0
        self.emniyet_kemeri_last_detected = 0
        self.el_last_detected = 0
        self.eldiven_last_detected = 0
        self.yanlis_eldiven_last_detected = 0


def main():
    model_path = "best (1).pt"
    video_path = "videos/5.mp4"
    output_path = "output_videos/5-8.mp4"

    video_processor = VideoProcessor.VideoProcessor(video_path, output_path)

    frame_count = 0

    update_interval = 0.5
    delay_duration = 3

    detection_state = DetectionState()

    yolo_model = YOLOModel.YOLOModel(model_path)

    detection_drawer = DetectionDrawer.DetectionDrawer(video_processor.width, video_processor.height)

    while video_processor.cap.isOpened():
        ret, frame = video_processor.cap.read()
        if not ret:
            break

        current_time = time.time()
        frame_count += 1
        if frame_count == 1:
            update_interval = 5

        if frame_count % update_interval == 0:  # Update every 1 second
            results = yolo_model.predict(frame)

            for result in results:
                for detection in result.boxes:
                    class_id = int(detection.cls)
                    class_name = yolo_model.model.names[class_id]

                    if class_name == "insan":
                        detection_state.insan_last_detected = current_time
                        print("frame count:", frame_count, "insan last:",
                              datetime.fromtimestamp(detection_state.insan_last_detected))
                    elif class_name == "baret":
                        detection_state.baret_last_detected = current_time
                        print("frame count:", frame_count, "baret last:",
                              datetime.fromtimestamp(detection_state.baret_last_detected))
                    elif class_name == 'emniyet-kemeri':
                        detection_state.emniyet_kemeri_last_detected = current_time
                        print("frame count:", frame_count, "emniyet kemeri last:",
                              datetime.fromtimestamp(detection_state.emniyet_kemeri_last_detected).strftime('%H:%M:%S'))
                    elif class_name == 'el':
                        detection_state.el_last_detected = current_time
                        print("frame count:", frame_count, "el last:",
                              datetime.fromtimestamp(detection_state.el_last_detected))
                    elif class_name == 'eldiven':
                        detection_state.eldiven_last_detected = current_time
                        print("frame count:", frame_count, "eldiven last:",
                              datetime.fromtimestamp(detection_state.eldiven_last_detected))
                    elif class_name == 'yanlis-eldiven':
                        detection_state.yanlis_eldiven_last_detected = current_time
                        print("frame count:", frame_count, "yanlis eldiven last:",
                              datetime.fromtimestamp(detection_state.yanlis_eldiven_last_detected))

        insan_okey = (current_time - detection_state.insan_last_detected) < delay_duration

        baret_okey = insan_okey and (current_time - detection_state.baret_last_detected) < delay_duration

        emniyet_kemeri_okey = insan_okey and (current_time - detection_state.emniyet_kemeri_last_detected) < delay_duration

        el_okey = insan_okey and (current_time - detection_state.el_last_detected) < delay_duration

        # For gloves to be positive, the hand must be completely negative
        eldiven_okey = insan_okey and (not el_okey) and (current_time - detection_state.eldiven_last_detected) < delay_duration

        yanlis_eldiven_okey = insan_okey and (current_time - detection_state.yanlis_eldiven_last_detected) < delay_duration

        detection_drawer.draw_table(frame)

        if insan_okey:
            if eldiven_okey and not el_okey and not yanlis_eldiven_okey:
                # If gloves are worn, no warning (X) is needed for hand and wrong gloves
                detection_drawer.update_status_gloves(frame, baret_okey, emniyet_kemeri_okey)
            elif not baret_okey and not emniyet_kemeri_okey and not eldiven_okey:
                # If helmet, seatbelt, and gloves are missing, show warnings (X) for all
                detection_drawer.update_status_no_error_hand(frame, el_okey, yanlis_eldiven_okey)
            elif el_okey and not yanlis_eldiven_okey:
                # If hand is detected, show warning (X) for gloves and - for wrong gloves
                detection_drawer.update_status_wrong_gloves(frame, baret_okey, emniyet_kemeri_okey)
            elif not el_okey and not eldiven_okey and not yanlis_eldiven_okey:
                # If hand, gloves, and wrong gloves are not detected, no warnings
                detection_drawer.update_status_hand(frame, baret_okey, emniyet_kemeri_okey)
            else:
                detection_drawer.update_status(frame, baret_okey, emniyet_kemeri_okey, el_okey, eldiven_okey, yanlis_eldiven_okey)
        else:
            # If no human is detected, no warnings for hand and wrong gloves
            detection_drawer.update_status_human(frame, insan_okey, baret_okey, emniyet_kemeri_okey, el_okey, eldiven_okey, yanlis_eldiven_okey)

        cv2.imshow('Frame', frame)
        video_processor.out.write(frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    video_processor.release()
    cv2.destroyAllWindows()

    print(f"Total frames processed: {frame_count}")

if __name__ == "__main__":
    main()
