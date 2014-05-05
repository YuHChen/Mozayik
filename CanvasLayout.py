from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class CanvasLayout(QLayout):
    def __init__(self, parent=None, margin=11, hSpacing=0, vSpacing=0):
        super(CanvasLayout, self).__init__(parent)
        self.hSpace = hSpacing
        self.vSpace = vSpacing
        self.margin = margin
        self.itemList = []

        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self.itemList.append(item)

    def horizontalSpacing(self):
        if self.hSpace >= 0:
            return self.hSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self.vSpace >= 0:
            return self.vSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]
        else:
            return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
        else:
            return None
        
    def expandingDirections(self):
        return Qt.Vertical | Qt.Horizontal

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0,0,width,0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)
        
    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize(0,0)
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2*self.margin, 2*self.margin)
        return size

    def doLayout(self, rect, testOnly):
        margins = self.getContentsMargins()
        left = margins[0]
        top = margins[1]
        right = margins[2]
        bottom = margins[3]
        effectiveRect = rect.adjusted(+left, +top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            if x == effectiveRect.x() and y == effectiveRect.y():
                lineHeight = item.sizeHint().height()
            #spaceX = self.horizontalSpacing()
            #if spaceX == -1:
                #spaceX = wid.style().layoutSpacing(QSizePolicy.Label, QSizePolicy.Label, Qt.Horizontal)
            #spaceY = self.verticalSpacing()
            #if spaceY == -1:
                #spaceY = wid.style().layoutSpacing(QSizePolicy.Label, QSizePolicy.Label, Qt.Vertical)
            nextX = x + item.sizeHint().width() #+ spaceX
            if nextX > effectiveRect.right():
                x = effectiveRect.x()
                y = y + lineHeight
                nextX = x + item.sizeHint().width()
                lineHeight = item.sizeHint().height()

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            #lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if not parent:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, 0, parent)
        else:
            return parent.spacing()


