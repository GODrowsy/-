from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QDateTime
import serial

import sys
import pymysql
import datetime as dt
import time
from PyQt5 import QtCore

from Cashier_management import lock_on, home_page


class CashierConsole(QMainWindow):
    lock_window = QtCore.pyqtSignal(str)
    home_window = QtCore.pyqtSignal()

    def __init__(self, user = 'qwe'):
        super(CashierConsole, self).__init__()
        self.user = user
        self.frist_time = time.strftime('%Y-%m-%d %H:%M:%S').split(' ')[1]
        print(self.frist_time)
        # 打开端口
        self.port = serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='E', stopbits=1, timeout=2)
        self.init_ui()

    def init_ui(self):
        self.port.write("close".encode("utf-8"))
        self.userimage = QPixmap('E:\\py project\\FaceRecognition\\user.jpeg')

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('收银员控制台')
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

        # # 创建菜单栏目录
        # menu_bar = self.menuBar()
        # fileMenu = menu_bar.addMenu('&File')
        # fileMenu.addAction(exitAction)

        self.user_name = QLabel(self)
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setFont(QFont("Roman times", 18))
        self.user_name.setGeometry(400, 50, 400, 100)

        self.user_lab = QLabel(self)
        self.user_lab.setGeometry(220, 250, 300, 400)

        self.btn1 = QPushButton('换班/收银员退出', self)
        self.btn1.setToolTip('收银员退出登录！')
        self.btn1.resize(220, 60)
        self.btn1.move(760, 400)
        # self.btn1.setFlat(True)

        self.btn2 = QPushButton('开锁', self)
        self.btn2.setToolTip('打开收银柜！')
        self.btn2.resize(220, 60)
        self.btn2.move(760, 550)

        self.btn3 = QPushButton('临时离开', self)
        self.btn3.setToolTip('收银员临时离开！')
        self.btn3.resize(220, 60)
        self.btn3.move(760, 700)
        # self.btn2.setFlat(True)

        self.timelabel = QLabel(self)
        self.timelabel.setGeometry(760, 300, 220, 60)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.btn1.clicked.connect(self.buttonClicked)
        # btn1.clicked.connect(self.sign_in())
        self.btn2.setShortcut('enter')
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

        if sender.text() == str('临时离开'):
            self.timer.stop()
            self.last_time = time.strftime('%Y-%m-%d %H:%M:%S').split(' ')[1]
            print(self.last_time)
            self.port.write("open".encode("utf-8"))
            self.save_work()
            self.port.close()
            self.onlock()
            # self.close()
        elif sender.text() == str('换班/收银员退出'):
            self.timer.stop()
            self.last_time = time.strftime('%Y-%m-%d %H:%M:%S').split(' ')[1]
            self.port.write("open".encode("utf-8"))
            self.save_work()
            self.port.close()
            self.onhome()
            # self.close()
        elif sender.text() == str('开锁'):
            print('lock_on')
            self.port.write("lockon".encode("utf-8"))
            # self.port.close()

    def onlock(self):
        # self.newWindow = lock_on.CashierConsole()
        # self.newWindow.show()
        self.lock_window.emit(self.user)

    def onhome(self):
        # self.homewin = home_page.HomePage()
        # self.homewin.show()
        self.home_window.emit()
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
        username = self.user + ' 欢迎使用收银控制台'

        painter = QPainter(self)
        pixmap = QPixmap('E:\\py project\\FaceRecognition\\background1.jpeg')

        self.user_lab.setPixmap(self.userimage)
        self.user_lab.setScaledContents(True)

        self.user_name.setText(username)
        self.user_name.setScaledContents(True)
        painter.drawPixmap(self.rect(), pixmap)

    def save_work(self):
        # 连接database
        conn = pymysql.connect(host='139.9.105.107', user='root', passwd='wzr152wzrA',
                               database='cashier_management', port=3306,
                               charset='utf8')

        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        print(self.user)
        sql_select = "SELECT id FROM cashier where name=%s;" % ("'"+self.user+"'")
        cursor.execute(sql_select)
        self.name_id = cursor.fetchone()[0]
        print(self.name_id)
        sql_insert = "INSERT INTO cashierwork(name_id,name,firsttime,lasttime,date)" \
                     " VALUES (%d,%s,%s,%s,%s);" \
                     % (int(self.name_id), "'"+self.user+"'", "'"+self.frist_time+"'",
                        "'"+self.last_time+"'", dt.date.today().strftime('"%Y-%m-%d"'))

        cursor.execute(sql_insert)
        conn.commit()
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = CashierConsole()
    page.show()
    sys.exit(app.exec_())
