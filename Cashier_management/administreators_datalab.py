from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QMainWindow, QLabel, QFrame, QApplication,
                             QTableWidgetItem, QPushButton, QLineEdit, QInputDialog,
                             QDesktopWidget, QTableWidget)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5 import QtCore

import pymysql
import sys
import datetime

import admin_FaceCollect


class DataLab(QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(DataLab, self).__init__()
        self.init_ui()

    def init_ui(self):

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('管理员人员管理')
        self.setWindowIcon(QIcon('E:\\py project\\FaceRecognition\\timg.jpg'))
        # 窗体大小
        self.resize(1200, 900)
        # 窗体居中
        self.center()

        self.user_name = QLabel(self)
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setFont(QFont("Roman times", 18))
        self.user_name.setGeometry(400, 0, 400, 100)
        self.user_name.setText('欢迎使用管理员人员管理')
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

        self.btn1 = QPushButton('增加管理员', self)
        self.btn1.setToolTip('管理员数据增加')
        self.btn1.resize(220, 60)
        self.btn1.move(480, 820)

        self.btn2 = QPushButton('删除管理员', self)
        self.btn2.setToolTip('管理员数据删除')
        self.btn2.resize(220, 60)
        self.btn2.move(720, 820)

        self.btn3 = QPushButton('刷新', self)
        self.btn3.setToolTip('数据刷新')
        self.btn3.resize(220, 60)
        self.btn3.move(960, 820)

        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)
        self.btn3.clicked.connect(self.buttonClicked)

    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + '被点击')

        if sender.text() == str('增加管理员'):
            self.onadd()
        elif sender.text() == str('删除管理员'):
            # 后面四个数字的作用依次是 初始值 最小值 最大值 步幅
            value, ok = QInputDialog.getText(self, "删除管理员", "请输入你要删除的管理员id：")
            self.del_date(value)
        elif sender.text() == str('刷新'):
            self.nowwin = DataLab()
            self.nowwin.show()
            self.close()

    def onadd(self):
        self.newWindow = add_win()
        self.newWindow.show()
        # self.switch_window.emit()

    def data_set(self):
        # 数据插入
        for i in range(self.row):
            for j in range(self.vol):
                if self.col_lst[j] != 'password':
                    temp_data = self.data[i][j]  # 临时记录，不能直接插入表格
                    data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                else:
                    temp_data = '******'  # 临时记录，不能直接插入表格
                    data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)

    def connect_sql(self):

        conn = pymysql.connect(host='139.9.105.107', user='root', passwd='wzr152wzrA',
                               database='cashier_management', port=3306,
                               charset='utf8')
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        # 定义要执行的SQL语句
        cursor.execute('select * from admin')
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

        admin_delete = "DELETE FROM admin WHERE id = %d;" \
                     % int(id)

        adface_delete = "DELETE FROM admin_face WHERE name_id = %d;" \
                     % int(id)
        cursor = conn.cursor()
        # 定义要执行的SQL语
        cursor.execute(admin_delete)
        cursor.execute(adface_delete)
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


class add_win(QWidget):
    switch_window = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super(add_win, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("管理员添加")
        self.resize(400, 400)
        self.center()

        self.IDLabel = QLabel("ID : ", self)
        self.IDLabel.setAlignment(Qt.AlignCenter)
        self.IDLabel.setGeometry(0, 0, 100, 100)

        self.IDLineEdit = QLineEdit(" ", self)
        self.IDLineEdit.setGeometry(120, 30, 200, 50)

        self.nameLabel = QLabel("name : ", self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setGeometry(0, 100, 100, 100)

        self.nameLineEdit = QLineEdit(" ", self)
        self.nameLineEdit.setGeometry(120, 130, 200, 50)

        self.passwordLabel = QLabel("passwork : ", self)
        self.passwordLabel.setAlignment(Qt.AlignCenter)
        self.passwordLabel.setGeometry(0, 200, 100, 100)

        self.passwordLineEdit = QLineEdit(" ", self)
        self.passwordLineEdit.setGeometry(120, 230, 200, 50)

        self.save_Btn = QPushButton('保存', self)
        self.save_Btn.setGeometry(50, 300, 100, 50)
        self.cancle_Btn = QPushButton('取消', self)
        self.cancle_Btn.setGeometry(250, 300, 100, 50)
        self.cancle_Btn.clicked.connect(self.quit)
        self.save_Btn.clicked.connect(self.addNum)

    def quit(self):
        self.close()

    def addNum(self):
        id = self.IDLineEdit.text()  # 获取文本框内容
        name = self.nameLineEdit.text()
        password = self.passwordLineEdit.text()

        self.add_sql(id, name, password)
        # self.switch_window.emit(name, id)
        self.add_face = admin_FaceCollect.GUI(name, id)
        self.add_face.show()
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

    def add_sql(self, id, name, password):

        conn = pymysql.connect(host='139.9.105.107', user='root', passwd='wzr152wzrA',
                               database='cashier_management', port=3306,
                               charset='utf8')

        sql_insert = "INSERT INTO admin VALUES (%d, %s, %s, %s);" \
                     % (int(id), "'"+name+"'", "'"+password+"'", datetime.datetime.now().strftime('"%Y-%m-%d %H:%M:%S"'))
        cursor = conn.cursor()
        # 定义要执行的SQL语
        cursor.execute(sql_insert)
        conn.commit()

        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()

#
# class Controller(object):
#
#     def __init__(self):
#         pass
#
#     def show_main(self):
#         self.datalab = DataLab()
#         self.datalab.switch_window.connect(self.show_add)
#         self.datalab.show()
#
#     def show_add(self):
#         self.addwin = add_win()
#         self.addwin.switch_window.connect(self.show_face_col)
#         self.addwin.show()
#
#     def show_face_col(self, name, id):
#         self.face_col = admin_FaceCollect.GUI(name, id)
#         self.addwin.close()
#         self.face_col.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    page = DataLab()
    page.show()
    sys.exit(app.exec_())