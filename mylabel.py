
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPen, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import QRect, Qt, pyqtSignal


class MyLabel(QLabel):
    focusInSignal = pyqtSignal(int, int)
    dropFileSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
        self.move = False  # 存在移动

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        # barHeight = self.bar.height()
        self.focusInSignal.emit(event.pos().x(), event.pos().y())
        self.move = True
        if self.flag:
            self.x1 = event.pos().x()
            self.y1 = event.pos().y()
            self.update()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False
        self.move = False
        print(self.x0, self.y0, self.x1, self.y1)
        self.x0, self.y0, self.x1, self.y1 = (0, 0, 0, 0)
        print(self.x0, self.y0, self.x1, self.y1)

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.flag and self.move:  # 只有当鼠标按下并且移动状态
            rect = QRect(self.x0, self.y0, (self.x1 - self.x0),
                         (self.y1 - self.y0))
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)
        # print(self.x0, self.y0, self.x1, self.y1)

    # 单击鼠标触发事件
    def mousePressEvent(self, event):
        # barHeight = self.bar.height()
        self.x0 = event.pos().x()
        self.y0 = event.pos().y()
        self.flag = True

    # 拖拽事件
    def dragEnterEvent(self, event: QDragEnterEvent):
        # 检查拖拽的数据中是否包含文件
        if event.mimeData().hasUrls():
            print(event.mimeData().hasUrls())
            for url in event.mimeData().urls():
                print(url)
                if url.scheme() == 'file':
                    event.acceptProposedAction()
                    return
        event.ignore()

    # 拖拽事件
    def dropEvent(self, event: QDropEvent):
        # 获取拖拽的文件URL
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.scheme() == 'file':
                    # 从URL获取文件路径
                    file_path = url.toLocalFile()
                    # 加载图片
                    self.dropFileSignal.emit(file_path)
                    print(file_path)
                    # 接收操作
                    event.acceptProposedAction()
                    return
        event.ignore()

    def drawROI(self, roi: list, drawType):
        return 
        print(roi)
        if drawType == 1:
            pass
        elif drawType == 0:
            painter = QPainter(self)
            count = int(len(roi)/4)
            rect = QRect()
            for i in range(count):
                index = i * 4
                rect.setRect(roi[index], roi[index + 1], roi[index + 2], roi[index + 3])
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                painter.drawRect(rect)
