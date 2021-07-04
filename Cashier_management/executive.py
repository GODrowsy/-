from Cashier_management_new import home_page
from Cashier_management_new import capture_distinguish
from Cashier_management_new import administrators_console
from Cashier_management_new import cashier_console
from Cashier_management_new import administreators_datalab
from Cashier_management_new import cashier_datalab
from Cashier_management_new import admin_FaceCollect
from Cashier_management_new import cashier_FaceCollect
from Cashier_management_new import cashier_work
from Cashier_management_new import lock_on

import sys
from PyQt5 import QtCore, QtWidgets

class Controller:

    def __init__(self):
        pass

    def show_home(self):
        self.home = home_page.HomePage()
        self.home.switch_window.connect(self.show_cap_dis)
        self.home.show()

    def show_cap_dis(self, user):
        print(user)
        self.cap_dis = capture_distinguish.GUI(user)
        if user == '收银员':
            self.cap_dis.switch_window.connect(self.show_cashier_con)
        elif user == '管理员':
            self.cap_dis.switch_window.connect(self.show_admin_con)
        # self.home.close()
        self.cap_dis.show()

    def show_cashier_con(self, user):
        self.cashier_con = cashier_console.CashierConsole(user)
        self.cashier_con.lock_window.connect(self.show_lock_on)
        self.cashier_con.home_window.connect(self.show_home)
        self.cap_dis.close()
        self.cashier_con.show()

    def show_lock_on(self, user):
        self.lock_on = lock_on.CashierConsole(user)
        self.lock_on.switch_window.connect(self.show_cap_dis)
        self.cashier_con.close()
        self.lock_on.show()


    def show_admin_con(self, user):
        self.admin_con = administrators_console.CashierConsole(user)
        self.admin_con.cashwork_window.connect(self.show_cashier_work)
        self.admin_con.cash_window.connect(self.show_cashier_data)
        self.admin_con.admin_window.connect(self.show_admin_data)
        self.cap_dis.close()
        self.admin_con.show()

    def show_cashier_data(self):
        # self.cashier_data = cashier_datalab.Controller.show_main()
        self.cashier_data = cashier_datalab.DataLab()
        self.cashier_data.show()

    def show_cashier_face_col(self, name, id):
        self.cashier_face_col = cashier_FaceCollect.GUI(name, id)
        self.cashier_face_col.show()

    def show_admin_data(self):
        # self.admin_data = administreators_datalab.Controller.show_main()
        self.admin_data = administreators_datalab.DataLab()
        self.admin_data.show()

    def show_admin_face_col(self, name, id):
        self.admin_face_col = admin_FaceCollect.GUI(name, id)
        self.admin_face_col.show()

    def show_cashier_work(self):
        self.cashier_work = cashier_work.DataLab()
        self.cashier_work.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_home()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()