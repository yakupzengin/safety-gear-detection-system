import YOLOModel
import VideoProcessor
import DetectionDrawer
import cv2
import time

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
    output_path = "output_videos/5-1.mp4"

    video_processor = VideoProcessor.VideoProcessor(video_path, output_path)

    frame_count = 0
    fps = video_processor.fps

    update_interval = 1  # Saniye başına güncelleme
    delay_duration = 2  # 2 saniyelik algılama süresi

    detection_state = DetectionState()

    yolo_model = YOLOModel.YOLOModel(model_path)

    detection_drawer = DetectionDrawer.DetectionDrawer(video_processor.width, video_processor.height)

    while video_processor.cap.isOpened():
        ret, frame = video_processor.cap.read()
        if not ret:
            break

        frame_count += 1
        current_time = time.time()

        detection_drawer.draw_table(frame)

        if frame_count % (update_interval * fps) == 0:  # Her saniyede bir kare al ve güncelle
            results = yolo_model.predict(frame)

            for result in results:
                for detection in result.boxes:
                    class_id = int(detection.cls)
                    class_name = yolo_model.model.names[class_id]

                    if class_name == "insan":
                        detection_state.insan_last_detected = current_time
                    elif class_name == "baret":
                        detection_state.baret_last_detected = current_time
                    elif class_name == 'emniyet-kemeri':
                        detection_state.emniyet_kemeri_last_detected = current_time
                    elif class_name == 'el':
                        detection_state.el_last_detected = current_time
                    elif class_name == 'eldiven':
                        detection_state.eldiven_last_detected = current_time
                    elif class_name == 'yanlis-eldiven':
                        detection_state.yanlis_eldiven_last_detected = current_time

        insan_okey = (current_time - detection_state.insan_last_detected) < delay_duration
        baret_okey = insan_okey and (current_time - detection_state.baret_last_detected) < delay_duration
        emniyet_kemeri_okey = insan_okey and (current_time - detection_state.emniyet_kemeri_last_detected) < delay_duration
        el_okey = insan_okey and (current_time - detection_state.el_last_detected) < delay_duration
        eldiven_okey = insan_okey and not el_okey and (current_time - detection_state.eldiven_last_detected) < delay_duration
        yanlis_eldiven_okey = insan_okey and (current_time - detection_state.yanlis_eldiven_last_detected) < delay_duration

        if insan_okey:
            if eldiven_okey and not el_okey and not yanlis_eldiven_okey:
                detection_drawer.update_status_gloves(frame, baret_okey, emniyet_kemeri_okey)
            elif not baret_okey and not emniyet_kemeri_okey and not eldiven_okey:
                detection_drawer.update_status_no_error_hand(frame, el_okey, yanlis_eldiven_okey)
            elif el_okey and not yanlis_eldiven_okey:
                detection_drawer.update_status_wrong_gloves(frame, baret_okey, emniyet_kemeri_okey)
            elif not el_okey and not eldiven_okey and not yanlis_eldiven_okey:
                detection_drawer.update_status_hand(frame, baret_okey, emniyet_kemeri_okey)
            else:
                detection_drawer.update_status(frame, baret_okey, emniyet_kemeri_okey, el_okey, eldiven_okey, yanlis_eldiven_okey)
        else:
            detection_drawer.update_status_human(frame, insan_okey, baret_okey, emniyet_kemeri_okey, el_okey, eldiven_okey, yanlis_eldiven_okey)

        cv2.imshow('Frame', frame)
        video_processor.out.write(frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    video_processor.release()
    cv2.destroyAllWindows()

    print(f"Toplam alınan kare sayısı: {frame_count}")

if __name__ == "__main__":
    main()
