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
    video_path = "videos/1.mp4"
    output_path = "output_videos/1.mp4"

    video_processor = VideoProcessor.VideoProcessor(video_path, output_path)

    frame_count = 0

    update_interval = 0.5
    delay_duration = 3

    detection_state = DetectionState()

    emniyet_kemeri_state = DetectionState()
    yolo_model = YOLOModel.YOLOModel(model_path)

    detection_drawer = DetectionDrawer.DetectionDrawer(video_processor.width, video_processor.height)

    while video_processor.cap.isOpened():
        ret, frame = video_processor.cap.read()
        if not ret:
            break

        # frame_count += 1  # frame sayacını artır
        current_time = time.time()
        frame_count += 1
        if frame_count == 1:
            update_interval=5


        if frame_count % update_interval == 0:  # her 1 saniyede bir güncelle
            results = yolo_model.predict(frame)

            for result in results:
                for detection in result.boxes:
                    class_id = int(detection.cls)
                    class_name = yolo_model.model.names[class_id]

                    if class_name == "insan":
                        detection_state.insan_last_detected = current_time # insanı en son  algıladığı time
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

        # ( şuanki zamandan - algıladığı zaman ) < ( 10 saniye de bir kotnrol etmek için verilen zaman dilimi )
            # eğer doğru çıkarsa 10 saniye içinde algılamıştır , okey.
            # fakat bu zaman dilimi daha büyükse 10 sn içinde algılamamıştır , not okey

        baret_okey = insan_okey and ( current_time - detection_state.baret_last_detected ) < delay_duration

        emniyet_kemeri_okey = insan_okey and ( current_time - detection_state.emniyet_kemeri_last_detected) < delay_duration

        el_okey = insan_okey and (current_time - detection_state.el_last_detected) < delay_duration

        # Eldivenin olumlu olması için elin tamamen olumsuz olması gerekir
        eldiven_okey = insan_okey  and  ( not el_okey ) and ( current_time - detection_state.eldiven_last_detected) < delay_duration

        yanlis_eldiven_okey = insan_okey and ( current_time - detection_state.yanlis_eldiven_last_detected) < delay_duration

        detection_drawer.draw_table(frame)

        if (insan_okey ):
            if eldiven_okey == True and el_okey == False and yanlis_eldiven_okey == False:
                # Eldiven giyilmişse, El ve Yanlış eldiven için uyarıya ( X e ) gerek yok ( - )
                detection_drawer.update_status_gloves(frame, baret_okey, emniyet_kemeri_okey)

            elif baret_okey == False and emniyet_kemeri_okey== False and  eldiven_okey == False:
                # Baret, Emniyet Kemeri ve Eldiven yoksa hepsine uyarı ( X ) ,diğerleri için duruma göre uyarı ver ya da -
                detection_drawer.update_status_no_error_hand(frame, el_okey, yanlis_eldiven_okey)

            elif el_okey == True and yanlis_eldiven_okey == False:        # El gözüktüğü için eldiven false.
                # El gözüküyorsa , Eldiven için uyarı yani X, yanlış eldiven için -
                detection_drawer.update_status_wrong_gloves(frame, baret_okey, emniyet_kemeri_okey)

            elif el_okey == False and eldiven_okey == False and yanlis_eldiven_okey == False:
                # El , Eldiven ve Yanlış eldiven gözükmüyorsa Bir uyarı vermeye gerek yok , üçü de -
                detection_drawer.update_status_hand(frame, baret_okey, emniyet_kemeri_okey)

            else:
                detection_drawer.update_status(frame, baret_okey, emniyet_kemeri_okey,  el_okey,eldiven_okey, yanlis_eldiven_okey)
        else :
            # İnsan gözükmüyorsa El ve Yanlış eldiven için uyarı vermeye gerek yok.
            detection_drawer.update_status_human(frame, insan_okey, baret_okey, emniyet_kemeri_okey,  el_okey,eldiven_okey, yanlis_eldiven_okey)

        cv2.imshow('Frame', frame)
        video_processor.out.write(frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    video_processor.release()
    cv2.destroyAllWindows()


    print(f"Toplam alınan kare sayısı: {frame_count}")

if __name__ == "__main__":
    main()