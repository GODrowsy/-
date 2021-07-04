from functools import partial
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLabel, QFrame, QApplication,
                             QTableWidgetItem, QPushButton, QLineEdit, QInputDialog,
                             QDesktopWidget, QTableWidget)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5 import QtCore

import pymysql
import sys
import datetime


class DataLab(QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(DataLab, self).__init__()
        self.init_ui()

    def init_ui(self):

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('收银员工作情况查询')
        self.setWindowIcon(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'))
        # 窗体大小
        self.resize(1200, 900)
        # 窗体居中
        self.center()

        self.user_name = QLabel(self)
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setFont(QFont("Roman times", 18))
        self.user_name.setGeometry(400, 0, 400, 100)
        self.user_name.setText('欢迎查看收银员工作情况')
        self.user_name.setScaledContents(True)

        # 数据库初始化
        self.connect_sql()

        # 插入表格
        self.MyTable = QTableWidget(self.row, self.vol, self)
        font = QFont('微软雅黑', 10)
        self.MyTable.setGeometry(0, 100, 1200, 700)

        # 设置字体、表头
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(self.col_lst)
        # 设置竖直方向表头不可见
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)

        self.data_set()

        self.btn1 = QPushButton('刷新', self)
        self.btn1.setToolTip('数据刷新')
        self.btn1.resize(220, 60)
        self.btn1.move(960, 820)

        self.btn2 = QPushButton('删除收银员记录', self)
        self.btn2.setToolTip('收银员记录删除')
        self.btn2.resize(220, 60)
        self.btn2.move(720, 820)

        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)

    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '被点击')

        if sender.text() == str('刷新'):
            self.nowwin = DataLab()
            self.nowwin.show()
            self.close()
        elif sender.text() == str('删除收银员记录'):
            value, ok = QInputDialog.getText(self, "删除收银员记录", "请输入你要删除记录的收银员id：")
            self.del_date(value)

    def data_set(self):
        # 数据插入
        for i in range(self.row):
            for j in range(self.vol):
                temp_data = self.data[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)

    def connect_sql(self):

        conn = pymysql.connect(host='139.9.105.107', user='root', passwd='wzr152wzrA',
                               database='cashier_management', port=3306,
                               charset='utf8')
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        # 定义要执行的SQL语句
        cursor.execute('select * from cashierwork')
        self.data = cursor.fetchall()

        # 数据列名
        self.col_lst = [tup[0] for tup in cursor.description]

        # 数据大小
        if len(self.data) == 0:
            self.row = 0
            self.vol = 0
        else:
            self.row = len(self.data)
            self.vol = len(self.data[0])


        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()

    def del_date(self, id):
        conn = pymysql.connect(host='139.9.105.107', user='root', passwd='wzr152wzrA',
                               database='cashier_management', port=3306,
                               charset='utf8')

        sql_delete = "DELETE FROM cashierwork WHERE id = %d;" \
                     % int(id)
        cursor = conn.cursor()
        # 定义要执行的SQL语
        sql = cursor.execute(sql_delete)
        conn.commit()

        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()

    def center(self):
        # 得到一个指定了主窗体形状的矩形
        qr = self.frameGeometry()
        # 指出显示器的屏幕分辨率并根据分辨率找出屏幕的中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 将矩形移动到屏幕中心
        qr.moveCenter(cp)
        # 窗体的左上角移动到矩形qr的左上角
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = DataLab()
    page.show()
    sys.exit(app.exec_())