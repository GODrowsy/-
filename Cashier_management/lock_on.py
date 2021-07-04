from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QDateTime

import sys
from Cashier_management import capture_distinguish
from PyQt5 import QtCore


class CashierConsole(QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, user = 'qwe'):
        super(CashierConsole, self).__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.userimage = QPixmap('E:\\py project\\FaceRecognition\\user.jpeg')

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('收银台已锁')
        self.setWindowIcon(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'))
        # 窗体大小
        self.resize(1200, 900)
        # 窗体居中
        self.center()

        self.user_name = QLabel(self)
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setFont(QFont("Roman times", 18))
        self.user_name.setGeometry(400, 50, 400, 100)

        self.btn = QPushButton('解锁', self)
        self.btn.setToolTip('人脸识别解锁继续工作！')
        self.btn.resize(220, 60)
        self.btn.move(490, 700)
        # self.btn2.setFlat(True)

        self.timelabel = QLabel(self)
        self.timelabel.setGeometry(400, 200, 400, 100)
        self.timelabel.setAlignment(Qt.AlignCenter)
        self.timelabel.setFont(QFont("Roman times", 18))
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.btn.clicked.connect(self.buttonClicked)

    def showTime(self):
        # 获取系统现在时间
        time = QDateTime.currentDateTime()
        # 设置系统时间显示格式
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        # 在标签上显示时间
        self.timelabel.setText(timeDisplay)

    def buttonClicked(self):
        print('12')
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '被点击')

        if sender.text() == str('解锁'):
            self.timer.stop()
            self.faceon()

    def faceon(self):
        self.switch_window.emit(str('收银员'))
        # self.rewin = capture_distinguish.GUI("收银员")
        # self.rewin.show()
        self.close()


    def center(self):
        # 得到一个指定了主窗体形状的矩形
        qr = self.frameGeometry()
        # 指出显示器的屏幕分辨率并根据分辨率找出屏幕的中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 将矩形移动到屏幕中心
        qr.moveCenter(cp)
        # 窗体的左上角移动到矩形qr的左上角
        self.move(qr.topLeft())


    def paintEvent(self, event):
        username = self.user + ' 收银员临时离开'

        painter = QPainter(self)
        pixmap = QPixmap('E:\\py project\\FaceRecognition\\background1.jpeg')

        self.user_name.setText(username)
        self.user_name.setScaledContents(True)

        self.timelabel.setScaledContents(True)
        painter.drawPixmap(self.rect(), pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = CashierConsole()
    page.show()
    sys.exit(app.exec_())
