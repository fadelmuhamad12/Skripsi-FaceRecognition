from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        #Update waktu dan hari
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        #Untuk memanggil updatean waktu dan hari
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        self.image = None

    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
        	self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        path = 'ImagesAttendance'
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)

        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # csv

        def mark_attendance(name):
            """
            :param name: detected face known or unknown one
            :return:
            """
            # Ini jika tombol klik button nya di klik maka tidak bisa diklik lg


            # self.ClcokInButton.setEnabled(False)
            if  self.ClockInButton.isChecked():
                self.ClockOutButton.setEnabled(False)
                self.ClockInButton.setEnabled(True)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'unknown'):
                            buttonReply = QMessageBox.question(self, "Selamat Datang" + name, 'Apakah anda ingin absen?' ,
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:

                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                f.writelines(f'\n{name},{date_time_string}, ')
                                self.ClockInButton.setChecked(False)

                                current_time = datetime.datetime.now().strftime("%I:%M:%p")

                                self.NameLabel.setText(name)
                                self.StatusLabel.setText('Mahsiswa Hadir')
                                # self.HoursLabel.setText('Measuring')
                                self.HoursLabel.setText(current_time)
                                self.MinLabel.setText('')

                                # # Untuk memunculkan confidence level HAAR CASCADE CLASSIFIER Baru ditambahin
                                # def detect_faces(self, img, labels=None, recognizer=None):
                                #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                #     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                                #     for (x, y, w, h) in faces:
                                #         roi_gray = gray[y:y + h, x:x + w]
                                #         roi_color = img[y:y + h, x:x + w]
                                #         id_, conf = recognizer.predict(roi_gray)
                                #         if conf > 70:
                                #             font = cv2.FONT_HERSHEY_SIMPLEX
                                #             name = labels[id_]
                                #             confidence = " {0}%".format(round(100 - conf))
                                #             cv2.putText(img, name + confidence, (x + 5, y - 5), font, 1,
                                #                         (255, 255, 255), 2)
                                #             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                #             return name, round(100 - conf)
                                #     return 'unknown', 0
                                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                #                                       minSize=(30, 30))
                                # for (x, y, w, h) in faces:
                                #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                #     confidence = str(
                                #         round(100 - (w * h) / (gray.shape[0] * gray.shape[1]) * 100, 2)) + '%'
                                #     cv2.putText(frame, confidence, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                #                 (0, 255, 0), 2)

                                #self.CalculateElapse(name)
                                #print('Yes clicked and detected')
                                self.Time1 = datetime.datetime.now()
                                #print(self.Time1)
                                self.ClockInButton.setEnabled(True)
                            else:
                                print('Belum di Klik')
                                self.ClockInButton.setEnabled(True)

            elif self.ClockOutButton.isChecked():
                self.ClockInButton.setEnabled(True)
                self.ClockOutButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'unknown'):
                            buttonReply = QMessageBox.question(self, 'Selamat datang' + name, "Apakah anda ingin absen?",
                                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:
                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                f.writelines(f'\n{name},{date_time_string},Dosen')
                                self.ClockOutButton.setChecked(False)

                                cuurent_time = datetime.datetime.now().strftime("%I:%M:%p")
                                self.NameLabel.setText(name)
                                self.StatusLabel.setText('Dosen Hadir')
                                self.HoursLabel.setText(cuurent_time)
                                self.Time2 = datetime.datetime.now()
                                #print(self.Time2)

                                # self.ElapseList(name)
                                # self.TimeList2.append(datetime.datetime.now())
                                # CheckInTime = self.TimeList1[-1]
                                # CheckOutTime = self.TimeList2[-1]
                                # self.ElapseHours = (CheckOutTime - CheckInTime)
                                # self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60)%60) + 'm')
                                # self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60**2)) + 'h')
                                self.ClockOutButton.setEnabled(True)
                            else:
                                print('Not clicked.')
                                self.ClockOutButton.setEnabled(True)

        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        # faces_cur_frame = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        distances = []
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            distances.append(face_dis)
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 128, 0), 1)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 128, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
                    match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
                    face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
                    distances.append(face_dis)
                    best_match_index = np.argmin(face_dis)
                    min_distance = face_dis[best_match_index]
                    confidence = round(((1 - min_distance) * 100), 2)
                    name = "unknown"
                    if match[best_match_index]:
                        name = class_names[best_match_index].upper()
                    y1, x2, y2, x1 = faceLoc
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 128, 0), 1)
                    cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 128, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    if confidence >= 50:
                        cv2.putText(frame, f"{confidence}% Terdaftar", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                    (0, 255, 0), 1)
                    else:
                        cv2.putText(frame, f"{confidence}% Tidak Di Ketahui", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX,
                                    0.5, (0, 0, 255), 1)
                    mark_attendance(name)
            mark_attendance(name)
        # Ini untuk menambahkan Level akurasinya atau level o%f confidence nya
        # for face_dis in distances:
        #     match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
        #     face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
        #     distances.append(face_dis)
        #     best_match_index = np.argmin(face_dis)
        #     min_distance = face_dis[best_match_index]
        #     confidence = round(((1 - min_distance) * 100), 2)
        #     if confidence >= 50:  # ini untuk menentukan apakah wajahnya dikenal atau tidak
        #         cv2.putText(frame, f"{confidence}% Terdaftar", (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
        #     else:
        #         cv2.putText(frame, f"{confidence}% Tidak Di Ketahui", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        return frame



    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


    def ElapseList(self,name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Clock In':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Clock Out':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time2 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)
                                #print(Time2)





    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
