import sys
import cv2
import numpy as np

from PIL import ImageQt, Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint

from FileDrawRect.MyLabel import MyLabel

class Video(object):
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = np.array([])

    def captureFrame(self):
        ret, frame =self.capture.read()
        return frame

    def captureNextFrame(self):
        ret, frame =self.capture.read()
        if ret is True:
            self.currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame,
                         width,
                         height,
                         QImage.Format_RGB888)
            img = QPixmap.fromImage(img)

            # self.previousFrame = self.currentFrame
            return img
        except:
            return None


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Face_Cascade = cv2.CascadeClassifier(
            r'E:\\anaconda\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt2.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(r'E:\\py project\\FaceRecognition\\trainer\\trainer.yml')

        self.setGeometry(250, 80, 800, 600)
        self.setWindowTitle('人脸识别')
        self.video = Video(cv2.VideoCapture(0, cv2.CAP_DSHOW))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
        self.videoFrame = MyLabel("摄像头准备中，请稍后......")
        self.videoFrame.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.videoFrame)

        self.ret, self.frame = self.video.capture.read()

    def play(self):
        try:
            self.video.captureNextFrame()
            self.videoFrame.drawingPermission(True)
            self.videoFrame.initDrawing(self.video.convertFrame())

            faces = self.Face_Cascade.detectMultiScale(self.video.currentFrame, minSize=(120, 120))
            for (x, y, w, h) in faces:
                # idnum, confidence = self.recognizer.predict(self.video.currentFrame[x: x + w,y: y + h])
                # cv2.waitKey(100)
                # print(idnum)

                self.videoFrame.drawRect(QPoint(x, y), QPoint(x + w, y + h))

            self.videoFrame.drawRect(QPoint(0, 0), QPoint(0, 0))
            self.videoFrame.setScaledContents(True)

        except TypeError:
            print('No Frame')

    def transImg(self, img):
        img = img.resize((self.label.width(), self.label.height()))
        return ImageQt.toqpixmap(img)

    def SHOW(self):
        self.show()

    def closeEvent(self, event):
        event.accept()
        cv2.VideoCapture(0, cv2.CAP_DSHOW).release()
        # cv2.destroyAllWindows()

    # def faceGet(self):
    #     self.recognizer.read('E:\\py project\\FaceRecognition\\trainer\\trainer.yml')
    #
    #     ret, frame = self.video.capture.read()
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     faces = self.Face_Cascade.detectMultiScale(gray, minSize=(120, 120))
    #
    #     return faces
    #
    #     for (x, y, w, h) in faces:
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         idnum, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
    #     #
        #     if confidence < 50:
        #         name = 'ltw' + str(idnum)
        #         Error = "{0}%".format(round(100 - confidence))
        #     else:
        #         name = 'unknown'
        #         Error = "{0}%".format(round(confidence))


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
