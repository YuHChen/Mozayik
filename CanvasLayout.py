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

    def itemAtPos(self, pos):
        for item in self.itemList:
            if item.geometry().contains(pos):
                return item.widget()
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
        else:
            return None

    def delete(self, item):
        for i in range(0, len(self.itemList)):
            if id(item) == id(self.itemList[i].widget()):
                self.takeAt(i).widget().close()
                break
        self.activate()

    def swapWidgets(self, item1, item2):
        pos1 = item1.pos()
        item1.geometry().moveTopLeft(item2.pos())
        item2.geometry().moveTopLeft(pos1)
        temp = QPixmap(item1.pixmap())
        item1.setPixmap(item2.pixmap())
        item2.setPixmap(temp)

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
        row = 0

        for item in self.itemList:
            wid = item.widget()
            wid.setRow(row)
            if x == effectiveRect.x() and y == effectiveRect.y():
                lineHeight = item.sizeHint().height()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(QSizePolicy.Label, QSizePolicy.Label, Qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(QSizePolicy.Label, QSizePolicy.Label, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right():
                x = effectiveRect.x()
                y = y + lineHeight# + spaceY
                row += 1
                wid.setRow(row)
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = item.sizeHint().height()

            geo = QRect(QPoint(x,y), item.sizeHint())

            unionRect = None

            for item2 in self.itemList[:len(self.itemList)-1]:
                wid2 = item2.widget()
                if x > effectiveRect.x():
                    geo.translate(-spaceX, 0)
                if wid2.getRow() == (wid.getRow()-1) and wid2.geometry().intersects(geo):
                    if unionRect is None:
                        unionRect = wid2.geometry().intersected(geo)
                    else:
                        unionRect = unionRect.united(wid2.geometry().intersected(geo))
                        #dx = wid2.geometry().intersected(geo).width()
                        #dy = wid2.geometry().intersected(geo).height()
                        #geo.translate(0, dy + spaceY)
                if  x > effectiveRect.x():
                    geo.translate(spaceX, 0)

            if unionRect is not None:
                geo.translate(0, unionRect.height() + spaceY)
            else:
                geo.translate(0, spaceY)

            if not testOnly:
                item.setGeometry(geo)

            x = nextX
            lineHeight = min(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if not parent:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, 0, parent)
        else:
            return parent.spacing()


