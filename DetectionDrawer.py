import cv2

class DetectionDrawer:
    def __init__(self, width, height):
        self.table_top_left = (10, 10)
        self.table_bottom_right = (225, 200)
        self.col1_start = self.table_top_left[0]

        self.col2_start = self.col1_start +150 # 160

        self.row_start = self.table_top_left[1] + 25
        self.row_end = self.table_bottom_right[1] - 20


        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (0, 0, 255)

    def draw_table(self, frame):
        frame[self.table_top_left[1]:self.table_bottom_right[1],
        self.table_top_left[0]:self.table_bottom_right[0]] = self.black
        cv2.rectangle(frame, self.table_top_left, self.table_bottom_right, self.red, thickness=2)


        cv2.line(frame, (self.col1_start, self.table_top_left[1]), (self.col1_start, self.table_bottom_right[1]),
                 self.red, thickness=2)

        cv2.line(frame, (self.col1_start + 150, self.table_top_left[1]), (self.col2_start, self.table_bottom_right[1]),
                 self.red, thickness=2)

        # Satır başlıkları
        cv2.putText(frame, 'Insan', (self.col1_start + 10, self.row_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.white,
                    1)
        cv2.putText(frame, 'Baret', (self.col1_start + 10, self.row_start + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.white,
                    1)
        cv2.putText(frame, 'Emniyet Kemeri', (self.col1_start + 10, self.row_start + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    self.white, 1)
        cv2.putText(frame, 'El', (self.col1_start + 10, self.row_start + 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.white, 1)
        cv2.putText(frame, 'Eldiven', (self.col1_start + 10, self.row_start + 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.white,
                    1)
        cv2.putText(frame, 'Yanlis eldiven', (self.col1_start + 10, self.row_start + 155), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    self.white, 1)

        # satır çizgileri
        for i in range(1, 6):
            cv2.line(frame, (self.col1_start, ( self.row_start + 15 )  + (i-1) * 30), # 45 , 60
                     (self.table_bottom_right[0], ( self.row_start + 15 ) + (i-1) * 30),
                     self.white, thickness=2)


    def update_beginning(self,frame):
        offset = 20

        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)

        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)

    def update_status_no_error_hand(self,frame, el_okey, yanlis_eldiven_okey):
        offset = 20

        # İnsan okey olma durumu
        cv2.line(frame, (self.col2_start + offset, self.row_start),
                     (self.col2_start + offset + 10, self.row_start + 10), self.green, 5)
        cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 10),
                     (self.col2_start + offset + 30, self.row_start - 10), self.green, 5)

        # Baret , Emniyet Kemeri ve Eldiven olumsuz

        # Baret X
        cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.red, 4)

        # Emniyet Kemeri X
        cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.red, 4)

        # Eldiven X
        cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.red, 4)

        if el_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 90),
                     (self.col2_start + offset + 10, self.row_start + 100), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 100),
                     (self.col2_start + offset + 30, self.row_start + 80), self.green, 5)
        else:
            # El gözükmüyorsa uyarıya gerek yok
            cv2.putText(frame, '-', (self.col2_start + offset + 8, self.row_start + 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)

        if yanlis_eldiven_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 150),
                     (self.col2_start + offset + 10, self.row_start + 160), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 160),
                     (self.col2_start + offset + 30, self.row_start + 140), self.green, 5)
        else:
            cv2.putText(frame, '-', (self.col2_start + offset + 8, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)

    def update_status(self, frame, baret_okey, emniyet_kemeri_okey,  el_okey,eldiven_okey, yanlis_eldiven_okey):

        offset = 20


        if insan_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start),
                     (self.col2_start + offset + 10, self.row_start + 10), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 10),
                     (self.col2_start + offset + 30, self.row_start - 10), self.green, 5)

        if baret_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 30),
                     (self.col2_start + offset + 10, self.row_start + 40), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 40),
                     (self.col2_start + offset + 30, self.row_start + 20), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if emniyet_kemeri_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 60),
                     (self.col2_start + offset + 10, self.row_start + 70), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 70),
                     (self.col2_start + offset + 30, self.row_start + 50), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if el_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 90),
                     (self.col2_start + offset + 10, self.row_start + 100), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 100),
                     (self.col2_start + offset + 30, self.row_start + 80), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if eldiven_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 120),
                     (self.col2_start + offset + 10, self.row_start + 130), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 130),
                     (self.col2_start + offset + 30, self.row_start + 110), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if yanlis_eldiven_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 150),
                     (self.col2_start + offset + 10, self.row_start + 160), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 160),
                     (self.col2_start + offset + 30, self.row_start + 140), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

    def update_status_gloves(self,frame, baret_okey, emniyet_kemeri_okey):
        offset = 20

        # İnsanın olumlu olma durumu
        cv2.line(frame, (self.col2_start + offset, self.row_start),
                (self.col2_start + offset + 10, self.row_start + 10), self.green, 5)
        cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 10),
                     (self.col2_start + offset + 30, self.row_start - 10), self.green, 5)

        if baret_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 30),
                     (self.col2_start + offset + 10, self.row_start + 40), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 40),
                     (self.col2_start + offset + 30, self.row_start + 20), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if emniyet_kemeri_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 60),
                     (self.col2_start + offset + 10, self.row_start + 70), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 70),
                     (self.col2_start + offset + 30, self.row_start + 50), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        # Eldiven olumlu olma durumu
        cv2.line(frame, (self.col2_start + offset, self.row_start + 120),
                 (self.col2_start + offset + 10, self.row_start + 130), self.green, 5)
        cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 130),
                 (self.col2_start + offset + 30, self.row_start + 110), self.green, 5)

        # El için uyarıya gerek yok
        cv2.putText(frame, '-', (self.col2_start + offset + 8, self.row_start + 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)

        # Yanlış eldiven için uyarıya gerek yok
        cv2.putText(frame, '-', (self.col2_start + offset + 8, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)
    def update_status_hand(self,frame, baret_okey, emniyet_kemeri_okey):

        offset = 20

        # İnsanın olumlu olma durumu
        cv2.line(frame, (self.col2_start + offset, self.row_start),
                     (self.col2_start + offset + 10, self.row_start + 10), self.green, 5)
        cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 10),
                     (self.col2_start + offset + 30, self.row_start - 10), self.green, 5)

        if baret_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 30),
                     (self.col2_start + offset + 10, self.row_start + 40), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 40),
                     (self.col2_start + offset + 30, self.row_start + 20), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if emniyet_kemeri_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 60),
                     (self.col2_start + offset + 10, self.row_start + 70), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 70),
                     (self.col2_start + offset + 30, self.row_start + 50), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)
        # El : False  -
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)
        # Eldiven : False -
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)
        # Yanlış Eldiven : False x-
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    self.white, 4)

    def update_status_wrong_gloves(self,frame, baret_okey, emniyet_kemeri_okey):
        offset = 20

        # insan olumlu olma durumu
        cv2.line(frame, (self.col2_start + offset, self.row_start),
                     (self.col2_start + offset + 10, self.row_start + 10), self.green, 5)
        cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 10),
                     (self.col2_start + offset + 30, self.row_start - 10), self.green, 5)

        if baret_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 30),
                     (self.col2_start + offset + 10, self.row_start + 40), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 40),
                     (self.col2_start + offset + 30, self.row_start + 20), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        if emniyet_kemeri_okey:
            cv2.line(frame, (self.col2_start + offset, self.row_start + 60),
                     (self.col2_start + offset + 10, self.row_start + 70), self.green, 5)
            cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 70),
                     (self.col2_start + offset + 30, self.row_start + 50), self.green, 5)
        else:
            cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        #el okey olma duurmu
        cv2.line(frame, (self.col2_start + offset, self.row_start + 90),
                     (self.col2_start + offset + 10, self.row_start + 100), self.green, 5)
        cv2.line(frame, (self.col2_start + offset + 10, self.row_start + 100),
                     (self.col2_start + offset + 30, self.row_start + 80), self.green, 5)

        # El gözüktüğü için eldiven kesinlikle False dir

        cv2.putText(frame, 'X', (self.col2_start + offset + 8, self.row_start + 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.red, 4)

        # if not yanlis_eldiven_okey:
        cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)


    def update_status_human(self,frame, insan_okey, baret_okey, emniyet_kemeri_okey, el_okey, eldiven_okey, yanlis_eldiven_okey):

        offset = 20

        if not insan_okey:
            cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)
            cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)
            cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)
            cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)
            cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)

            cv2.putText(frame, '-', (self.col2_start + offset + 5, self.row_start + 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        self.white, 4)
