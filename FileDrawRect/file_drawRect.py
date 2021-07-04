import sys
from PIL import ImageQt, Image
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from main_ui import Ui_MainWindow

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        img = Image.open(r'E:\\py project\\FaceRecognition\\background.jpeg')
        img = self.transImg(img)
        self.label.setPixmap(img)

        self.flagPaint = False

        self.pushButton.clicked.connect(self.getImage)
        self.pushButton_2.clicked.connect(self.saveImage)

    def getImage(self):
        fdir, ftypr = QFileDialog.getOpenFileName(self,
                                                  "选择图片",
                                                  "../",
                                                  "Image Files (*.png *.jpg *.jpeg)")

        img = Image.open(fdir)
        img = self.transImg(img)
        self.label.setPixmap(img)

        self.label.initDrawing(img)
        self.label.drawingPermission(True)
        self.flagPaint = True

    def saveImage(self):
        if self.flagPaint:
            img = self.label.pix.toImage()
            fdir, ftypr = QFileDialog.getOpenFileName(self,
                                                      "保存图片",
                                                      "../",
                                                      "Image Files (*.jpg)")
            img.save(fdir)

    def transImg(self, img):
        img = img.resize((self.label.width(), self.label.height()))
        return ImageQt.toqpixmap(img)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())