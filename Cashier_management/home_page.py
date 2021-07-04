from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
# from gevent.libev.corecext import SIGNAL, time

import sys

from Cashier_management import capture_distinguish


class HomePage(QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(HomePage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.administratorsimage = QPixmap('E:\\py project\\FaceRecognition\\administrators.jpeg')
        self.userimage = QPixmap('E:\\py project\\FaceRecognition\\user.jpeg')

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('首页')
        self.setWindowIcon(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'))
        # 窗体大小
        self.resize(1200, 900)
        # 窗体居中
        self.center()

        # 创建菜单栏
        exitAction = QAction(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'), '&关闭', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        # 菜单栏事件
        exitAction.triggered.connect(qApp.quit)

        # 创建菜单栏目录
        menu_bar = self.menuBar()
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # 创建工具栏目录
        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exitAction)

        # 这个静态方法为tooltip设置了10px的Sanserif字体
        # QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('This is a <b>QWidget</b> widget')
        self.administrators_lab = QLabel(self)
        self.administrators_lab.setGeometry(120, 200, 300, 400)

        self.user_lab = QLabel(self)
        self.user_lab.setGeometry(720, 200, 300, 400)

        # col = QColor(0, 0, 0)
        # self.frm = QFrame(self)
        # self.frm.setStyleSheet("QWidget { background-color: %s }"
        #                        % col.name())

        # self.frm.setGeometry(160, 200, 200, 200)

        self.btn1 = QPushButton('管理员', self)
        self.btn1.setToolTip('管理员登录！')
        self.btn1.resize(220, 60)
        self.btn1.move(160, 700)

        # layout = QGridLayout(self)
        btn2 = QPushButton('收银员', self)
        btn2.setToolTip('收银员登录！')
        btn2.resize(220, 60)
        btn2.move(760, 700)

        self.btn1.clicked.connect(self.buttonClicked)
        # btn1.clicked.connect(self.sign_in())
        btn2.clicked.connect(self.buttonClicked)

    # def sign_in(self):
    #
    #     fr = FaceRecognition()
    #     fr.RecognitionFace()

    def buttonClicked(self):

        username = '收银员'
        administratorsname = '管理员'

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '被点击')

        self.onclick(sender.text())

        # if sender.text() == str(administratorsname):
        #     self.admin()

    def onclick(self, user):
        # self.newWindow = capture_distinguish.GUI(user)
        # self.newWindow.show()

        self.switch_window.emit(user)

    def center(self):
        # 得到一个指定了主窗体形状的矩形
        qr = self.frameGeometry()
        # 指出显示器的屏幕分辨率并根据分辨率找出屏幕的中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 将矩形移动到屏幕中心
        qr.moveCenter(cp)
        # 窗体的左上角移动到矩形qr的左上角
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):

        painter = QPainter(self)
        pixmap = QPixmap('E:\\py project\\FaceRecognition\\background.jpeg')

        self.administrators_lab.setPixmap(self.administratorsimage)
        self.administrators_lab.setScaledContents(True)
        self.user_lab.setPixmap(self.userimage)
        self.user_lab.setScaledContents(True)
        painter.drawPixmap(self.rect(), pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = HomePage()
    page.show()
    sys.exit(app.exec_())
