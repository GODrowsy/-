from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5 import QtCore

import sys

from Cashier_management import administreators_datalab, cashier_datalab, cashier_work


class CashierConsole(QMainWindow):
    cashwork_window = QtCore.pyqtSignal()
    cash_window = QtCore.pyqtSignal()
    admin_window = QtCore.pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.userimage = QPixmap('E:\\py project\\FaceRecognition\\user.jpeg')

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('管理员控制台')
        self.setWindowIcon(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'))
        # 窗体大小
        self.resize(1200, 900)
        # 窗体居中
        self.center()

        # # 创建菜单栏
        # exitAction = QAction(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'), '&关闭', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # # 菜单栏事件
        # exitAction.triggered.connect(qApp.quit)
        #
        # # 创建菜单栏目录
        # menu_bar = self.menuBar()
        # fileMenu = menu_bar.addMenu('&File')
        # fileMenu.addAction(exitAction)

        self.user_name = QLabel(self)
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setFont(QFont("Roman times", 18))
        self.user_name.setGeometry(400, 50, 400, 100)

        self.user_lab = QLabel(self)
        self.user_lab.setGeometry(220, 320, 300, 400)

        self.btn1 = QPushButton('收银员工作情况', self)
        self.btn1.setToolTip('检查收银员的工作情况')
        self.btn1.resize(220, 60)
        self.btn1.move(760, 500)

        self.btn2 = QPushButton('收银员人员管理', self)
        self.btn2.setToolTip('收银员的人员情况、注册、修改以及删除')
        self.btn2.resize(220, 60)
        self.btn2.move(760, 700)

        self.btn3 = QPushButton('管理员人员管理', self)
        self.btn3.setToolTip('管理员的人员情况、注册、修改以及删除')
        self.btn3.resize(220, 60)
        self.btn3.move(760, 300)

        self.timelabel = QLabel(self)
        self.timelabel.setGeometry(760, 200, 220, 60)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)
        self.btn3.clicked.connect(self.buttonClicked)

    def showTime(self):
        # 获取系统现在时间
        time = QDateTime.currentDateTime()
        # 设置系统时间显示格式
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        # 在标签上显示时间
        self.timelabel.setText(timeDisplay)


    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '被点击')

        if sender.text() == str('管理员人员管理'):
            self.onadmin()
            # self.close()
        elif sender.text() == str('收银员人员管理'):
            self.oncashier()
        elif sender.text() == str('收银员工作情况'):
            self.oncashwork()

    def oncashwork(self):
        # self.cashworkwin = cashier_work.DataLab()
        # self.cashworkwin.show()
        self.cashwork_window.emit()

    def oncashier(self):
        # self.cashwin = cashier_datalab.DataLab()
        # self.cashwin.show()
        self.cash_window.emit()

    def onadmin(self):
        # self.adminWindow = administreators_datalab.DataLab()
        # self.adminWindow.show()
        self.admin_window.emit()


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
        username = self.user + ' 欢迎使用管理员控制台'

        painter = QPainter(self)
        pixmap = QPixmap('E:\\py project\\FaceRecognition\\background1.jpeg')

        self.user_lab.setPixmap(self.userimage)
        self.user_lab.setScaledContents(True)

        self.user_name.setText(username)
        self.user_name.setScaledContents(True)
        painter.drawPixmap(self.rect(), pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = CashierConsole('ltw')
    page.show()
    sys.exit(app.exec_())
