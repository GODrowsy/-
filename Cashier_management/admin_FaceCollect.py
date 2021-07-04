import sys
import cv2
import numpy as np
import face_recognition
import pymysql

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
    switch_window = QtCore.pyqtSignal()

    def __init__(self, name, id):
        super().__init__()
        self.name = name
        self.name_id = id
        self.Face_Cascade = cv2.CascadeClassifier(
            r'E:\\anaconda\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt2.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(r'E:\\py project\\FaceRecognition\\trainer\\trainer.yml')

        self.setGeometry(250, 80, 800, 600)
        self.setWindowTitle('人脸识别')
        self.video = Video(cv2.VideoCapture(0))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()

        self.count = 0

        self.videoFrame = MyLabel("摄像头准备中，请稍后......")
        self.videoFrame.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.videoFrame)

        self.ret, self.frame = self.video.capture.read()

    def play(self):
        self.video.captureNextFrame()
        self.videoFrame.drawingPermission(True)
        self.videoFrame.initDrawing(self.video.convertFrame())

        faces = self.Face_Cascade.detectMultiScale(self.video.currentFrame, minSize=(120, 120))

        for (x, y, w, h) in faces:
            # 人脸画框
            self.videoFrame.drawRect(QPoint(x, y), QPoint(x + w, y + h))

            # 返回图像中每个面的128维人脸编码
            # 图像中可能存在多张人脸，取下标为0的人脸编码，表示识别出来的最清晰的人脸
            if len(face_recognition.face_encodings(self.video.currentFrame)) != 0:
                image_face_encoding = face_recognition.face_encodings(self.video.currentFrame)[0]
                # print(np.shape(image_face_encoding))

                # 将numpy array类型转化为列表
                encoding__array_list = image_face_encoding.tolist()

                # 将列表里的元素转化为字符串
                encoding_str_list = [str(i) for i in encoding__array_list]

                # 拼接列表里的字符串
                encoding_str = ','.join(encoding_str_list)

                print(encoding_str)

                self.save_encoding(encoding_str, self.name, self.name_id)
                self.count = self.count + 1

        if self.count >= 10:
            self.close()
            self._timer.stop()

        print(self.count)


        self.videoFrame.drawRect(QPoint(0, 0), QPoint(0, 0))
        self.videoFrame.setScaledContents(True)


    # 人脸特征信息保存
    def save_encoding(self, encoding_str, name, id):
        # 创建数据库连接对象
        conn = pymysql.connect(
            # 数据库的IP地址
            host="139.9.105.107",
            # 数据库用户名称
            user="root",
            # 数据库用户密码
            password="wzr152wzrA",
            # 数据库名称
            db="cashier_management",
            # 数据库端口名称
            port=3306,
            # 数据库的编码方式 注意是utf8
            charset="utf8"
        )

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()

        # SQL插入语句
        insert_sql = "insert into admin_face(name_id,name,encoding) values(%d,%s,%s)"
        try:
            # 执行sql语句
            cursor.execute(insert_sql % (int(id), "'"+name+"'", "'"+encoding_str+"'"))
            # 提交到数据库执行
            conn.commit()
        except Exception as e:
            # 如果发生错误则回滚并打印错误信息
            conn.rollback()
            print(e)

        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()

    def transImg(self, img):
        img = img.resize((self.label.width(), self.label.height()))
        return ImageQt.toqpixmap(img)

    def SHOW(self):
        self.show()

    def closeEvent(self, event):
        event.accept()
        cv2.VideoCapture(0, cv2.CAP_DSHOW).release()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    ex = GUI('ltw','123')
    ex.show()
    sys.exit(app.exec_())
