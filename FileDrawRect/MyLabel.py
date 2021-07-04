from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPixmap, QPen, QFont

class MyLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.drawable = False

    def drawingPermission(self, a):
        if isinstance(a, bool):
            self.drawable = a

    def initDrawing(self, img):
        self.pix =img
        self.tmpPix = self.pix.copy()
        self.lastPoint = QPoint()
        self.endPoint = QPoint()

    def drawRect(self, lastPoint, endPoint):
        if self.drawable:
            self.pix = self.tmpPix.copy()
            pp = QPainter(self.pix)
            pp.setPen(QPen(Qt.blue, 5))
            pp.drawRect(lastPoint.x(), lastPoint.y(),
                        endPoint.x() - lastPoint.x(),
                        endPoint.y() - lastPoint.y())
            # pp.setFont(QFont('SimSun', 20))
            # pp.drawText(0, 0, s)
            self.update()
            self.tmpPix = self.pix
            self.lastPoint = lastPoint
            self.endPoint = endPoint

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.drawable:
            pp = QPainter(self)
            pp.begin(self)
            pp.drawPixmap(self.rect(), self.pix)
            pp.end()

    # def mousePressEvent(self, event):
    #     super().mousePressEvent(event)
    #     if self.drawable:
    #         if event.buttons() and Qt.LeftButton:
    #             self.endPoint = event.pos()
    #
    #             self.pix = self.tmpPix.copy()
    #             pp = QPainter(self.pix)
    #             pp.setPen(QPen(Qt.blue, 5))
    #             pp.drawRect(self.lastPoint.x(), self.lastPoint.y(),
    #                         self.endPoint.x() - self.lastPoint.x(),
    #                         self.endPoint.y() - self.lastPoint.y())
    #             self.update()
    #
    # def mouseReleaseEvent(self, event):
    #     super().mouseReleaseEvent(event)
    #     if self.drawable:
    #         if event.buttons() == Qt.LeftButton:
    #             self.tmpPix = self.pix
