from turtle import pos
from PyQt5.QtWidgets import QApplication, QFileDialog, QAction, QLabel, QLineEdit, QLineEdit, QComboBox, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen, QDoubleValidator, QIntValidator
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QRect, QRegExp
import sys

# from colorama import init
from mylabel import MyLabel


class MainProcess():
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.ui = loadUi('test.ui')
        self.statusLabel: QLabel = QLabel()
        self.ui.statusbar.addWidget(self.statusLabel)
        self.statusLabel.setText('init')
        # input valid set
        self.ui.lineEditZoomRatio.setValidator(QDoubleValidator(self. ui.lineEditZoomRatio))
        self.ui.lineEditPicH.setValidator(QIntValidator(self.ui.lineEditPicH))
        self.ui.lineEditPicW.setValidator(QIntValidator(self.ui.lineEditPicW))

        # slot
        self.ui.actionSave.triggered.connect(self.saveImg)
        self.ui.actionOpen.triggered.connect(self.openImg)

        zoomratio: QLineEdit = self.ui.lineEditZoomRatio
        picSizeH: QLineEdit = self.ui.lineEditPicH
        picSizeW: QLineEdit = self.ui.lineEditPicW
        roi: QTextEdit = self.ui.textEditROI
        zoomratio.textChanged.connect(self.drawRect)
        picSizeH.textChanged.connect(self.drawRect)
        picSizeW.textChanged.connect(self.drawRect)
        roi.textChanged.connect(self.drawRect)

        labelimg: MyLabel = self.ui.labelShowImg
        labelimg.focusInSignal.connect(self.updateStatusBarInfo)
        labelimg.dropFileSignal.connect(self.dropShowImg)

    def drawRect(self):
        isRoiValid = False
        if self.ui.textEditROI.toPlainText():
            pat = r'(\d+,){1,}\d+'
            reg_exp = QRegExp(pat)
            if reg_exp.exactMatch(self.ui.textEditROI.toPlainText()):
                isRoiValid = True

        isInputValid = (bool(self.ui.lineEditZoomRatio.text()) & bool(self.ui.lineEditPicH.text()) &
                        bool(self.ui.lineEditPicW.text()) & isRoiValid)
        if isInputValid is not True:
            self.statusBarInfoUpdate('输入参数错误')
            return
        zoomRatio = float(self.ui.lineEditZoomRatio.text())
        picH = int(self.ui.lineEditPicH.text())
        picW = int(self.ui.lineEditPicW.text())
        posture = self.ui.comboBoxPosture.currentIndex()
        drawType = self.ui.comboBoxPosture.currentIndex()
        roi = [int(digit) for digit in str.split(self.ui.textEditROI.toPlainText(), ',')]
        print(zoomRatio, picH, picW, posture, drawType, roi)

        if drawType == 1:
            pass
        elif drawType == 0:
            painter = QPainter(self.img)
            # print(self.img)
            count = int(len(roi)/4)
            rect = QRect()
            # print(count, range(count))
            for i in range(count):
                print(i)
                index = i * 4
                rect.setRect(roi[index], roi[index + 1], roi[index + 2], roi[index + 3])
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                painter.drawRect(rect)
                self.updateImge()

    # 退拽图片到画框显示
    def dropShowImg(self, filePath):
        fileExtName = str.split(filePath, '.')[-1]
        if fileExtName == 'jpg' or fileExtName == 'png' or fileExtName == 'png':
            self.showImgByPath(filePath)
        else:
            self.statusBarInfoUpdate(str(filePath + ' 不是图片文件'))

    def updateStatusBarInfo(self, x: int, y: int):
        self.statusBarInfoUpdate(coordinate=[x, y])

    # 显示UI
    def uiShow(self):
        self.ui.show()

    # 退出软件
    def uiExit(self):
        sys.exit(self.app.exec())

    # QPixmap图片显示在labelShowImg
    def updateImge(self):
        showLabel: MyLabel = self.ui.labelShowImg
        pix = self.img.scaled(showLabel.size().width() - 4, showLabel.size().height() - 4,
                              Qt.KeepAspectRatio,  Qt.SmoothTransformation)
        showLabel.setPixmap(pix)
        showLabel.setScaledContents(True)
        showLabel.setCursor(Qt.CrossCursor)

    # debug 布局中的空间宽度
    def get_widget_widths(self, layout: QHBoxLayout):
        widget_widths = []
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            print('debug-', i)
            if widget:
                print(widget.objectName)
                size_hint = widget.sizeHint()
                widget_widths.append(size_hint.width())
            else:
                print('=====')
        return widget_widths

    # 通过路径打开图片并显示
    def showImgByPath(self, file_name):
        self.img = QPixmap(file_name)
        self.updateImge()

    # 打开图片并显示到labelShowImg
    def openImg(self):
        file_name = QFileDialog.getOpenFileName(
            None, "选择文件", ".\\", "图片 (*.jpg);;图片 (*.png);;所有文件 (*)")
        print(file_name)
        self.showImgByPath(file_name[0])

    # 更新状态栏
    def statusBarInfoUpdate(self, info=None, coordinate=None):
        if coordinate is not None:
            infoStr = 'x: ' + str(coordinate[0]) + ' y: ' + str(coordinate[1])
            self.statusLabel.setText(infoStr)
        elif info is not None:
            self.statusLabel.setText(info)

    # 保存LabelShow的图片
    def saveImg(self):
        showImg: MyLabel = self.ui.labelShowImg
        pixmap = showImg.pixmap()
        fileName = QFileDialog.getSaveFileName(None, '保存文件', '.\\', "图片 (*.jpg)")
        pixmap.save(fileName[0])


if __name__ == "__main__":
    print('hello')
    proc = MainProcess()

    proc.uiShow()
    proc.uiExit()
