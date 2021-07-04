import time
import sys
import cv2
import numpy as np
import pymysql
import face_recognition
from collections import Counter

from PIL import ImageQt, Image, ImageFont, ImageDraw
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint

from FileDrawRect.MyLabel import MyLabel
from Cashier_management import administrators_console
from Cashier_management import cashier_console


class Video(object):
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = np.array([])

    def captureOpen(self):

        return self.capture.isOpened()

    def captureFrame(self):
        ret, frame = self.capture.read()
        return frame

    def captureNextFrame(self):
        ret, frame = self.capture.read()
        if ret is True:
            self.currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # print(frame)
        return ret

    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame,
                         width,
                         height,
                         QImage.
                         Format_RGB888)
            img = QPixmap.fromImage(img)

            # self.previousFrame = self.currentFrame
            return img
        except Exception as e:
            print(e)
            return None


class GUI(QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, user = '管理员'):
        super().__init__()
        self.user = user
        self.Face_Cascade = cv2.CascadeClassifier(
            r'E:\\anaconda\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt2.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(r'E:\\py project\\FaceRecognition\\trainer\\trainer.yml')
        self.known_face_encodings = []
        self.known_face_names = []

        if self.user == "管理员":
            self.get_admin_info()
        elif self.user == "收银员":
            self.get_cashier_info()
        print(self.user)
        print(self.known_face_names)

        self.setGeometry(250, 80, 800, 600)
        self.setWindowTitle('人脸识别')
        #self.video = Video(cv2.VideoCapture(0, cv2.CAP_DSHOW))
        self.video = Video(cv2.VideoCapture(0))
        time.sleep(1)
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
            if self.video.captureNextFrame() is True:
                self.videoFrame.drawingPermission(True)
                self.videoFrame.initDrawing(self.video.convertFrame())

                faces = self.Face_Cascade.detectMultiScale(self.video.currentFrame, minSize=(120, 120))
                for (x, y, w, h) in faces:
                    self.videoFrame.drawRect(QPoint(x, y), QPoint(x + w, y + h))
                    face_name = self.load_image()
                    print(face_name[0])
                    if face_name[0] != "Unknow":

                        face_name_now = Counter(face_name).most_common(1)[0][0]
                        print(Counter(face_name).most_common(1)[0][1])
                        if Counter(face_name).most_common(1)[0][1] <= 8:
                            continue
                        print(face_name_now)
                        # if self.user == "管理员":
                        #     self.adminwin = administrators_console.CashierConsole(face_name_now)
                        #     self.adminwin.show()
                        # elif self.user == "收银员":
                        #     self.cashierwin = cashier_console.CashierConsole(face_name_now)
                        #     self.cashierwin.show()
                        # self.close()

                        self.switch_window.emit(face_name_now)
                        self._timer.stop()

                self.videoFrame.drawRect(QPoint(0, 0), QPoint(0, 0))
                self.videoFrame.setScaledContents(True)


        except Exception as e:
            print(e)

    def transImg(self, img):
        img = img.resize((self.label.width(), self.label.height()))
        return ImageQt.toqpixmap(img)

    def SHOW(self):
        self.show()

    def closeEvent(self, event):
        event.accept()
        cv2.VideoCapture(0, cv2.CAP_DSHOW).release()

    def load_image(self):

        # 利用opencv的缩放函数改变摄像头图像的大小
        small_frame = cv2.resize(self.video.captureFrame(), (0, 0), fx=0.25, fy=0.25)

        #  opencv的图像是BGR格式的，将其转化为RGB格式
        rgb_small_frame = small_frame[:, :, ::-1]

        # 使用默认的HOG模型查找图像中的所有人脸
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

        # 返回128维人脸编码，即人脸特征
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        # 将得到的人脸特征与数据库中的人脸特征集合进行比较，相同返回True，不同返回False
        for face_encoding in face_encodings:

            if len(self.known_face_encodings) != 0:
                # matches：一个返回值为True或者False值的列表，该表指示了known_face_encodings列表的每个成员的匹配结果
                # tolerance：越小对比越严格，官方说法是0.6为典型的最佳值，也是默认值
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.45)

                if True in matches:

                    # first_match_index = matches.index(True)
                    # name = self.known_face_names[first_match_index]
                    # print('已存在')

                    for index, value in enumerate(matches):
                        if value == True:
                            name = self.known_face_names[index]
                            face_names.append(name)
                else:
                    # 默认为unknown
                    name = "Unknow"
                    # print('不存在')
                    face_names.append(name)

        return face_names

    def get_admin_info(self):
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

        # SQL查询语句
        sql = "select * from admin_face"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # 返回的结果集为元组
            for row in results:
                name = row[2]
                encoding = row[3]
                # print("name=%s,encoding=%s" % (name, encoding))
                # 将字符串转为numpy ndarray类型，即矩阵
                # 转换成一个list
                dlist = encoding.strip(' ').split(',')
                # 将list中str转换为float
                dfloat = list(map(float, dlist))
                arr = np.array(dfloat)

                # 将从数据库获取出来的信息追加到集合中
                self.known_face_encodings.append(arr)
                self.known_face_names.append(name)

        except Exception as e:
            print(e)

            # 关闭数据库连接
            conn.close()

    def get_cashier_info(self):
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

        # SQL查询语句
        sql = "select * from cashier_face"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # 返回的结果集为元组
            for row in results:
                name = row[2]
                encoding = row[3]
                # print("name=%s,encoding=%s" % (name, encoding))
                # 将字符串转为numpy ndarray类型，即矩阵
                # 转换成一个list
                dlist = encoding.strip(' ').split(',')
                # 将list中str转换为float
                dfloat = list(map(float, dlist))
                arr = np.array(dfloat)

                # 将从数据库获取出来的信息追加到集合中
                self.known_face_encodings.append(arr)
                self.known_face_names.append(name)

        except Exception as e:
            print(e)

            # 关闭数据库连接
            conn.close()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
