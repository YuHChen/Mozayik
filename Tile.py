from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Viewer import *

class Tile(QLabel):
    def __init__(self,fileName,pixmap=None,parent=None):
        super(Tile,self).__init__(parent)
        if(pixmap is None):
            self.setPixmap(QPixmap(str(fileName)))
        else:
            self.setPixmap(pixmap)
        self.show
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.name = fileName

        #size = QSize(self.pixmap().width(),self.pixmap().height())
        #self.setMaximumSize(size)
        #self.setMinimumSize(size)

        #mouse press event 
        self.canCopy = False
        self.canMove = False
        self.canStretch = False
        self.isStretchingH = False
        self.isStretchingV = False
        self.isMouseDown = False
        self.mousePosn = QPoint()
        self.mouseTime = QTime()

        #layout
        self.row = 0

    def __str__(self):
        return self.name

    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return (str(self) == str(other))
        else:
            return False

    def __ne__(self,other):
        return not self == other

    def __getattr__(self,name):
        return self

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setCanCopy(self, val):
        self.canCopy = val
        
    def setCanMove(self, val):
        self.canMove = val

    def setCanStretch(self, val):
        self.canStretch = val

    def setRow(self, val):
        self.row = val

    def getRow(self):
        return self.row

    def sizeHint(self):
        size = QSize(self.pixmap().width(),self.pixmap().height())
        return size

    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            #print("mouse left click at x:{} y:{}".format(event.pos().x(),event.pos().y()))
            self.isMouseDown = True
            self.mousePosn = event.pos()
            self.mouseTime.start()
            if self.canStretch:
                ex = event.pos().x()
                ey = event.pos().y()
                x = self.size().width()
                y = self.size().height()
                if ex < 15 or ex > x-15: 
                    #print("can stretch horizontally")
                    self.isStretchingH = True
                if ey < 15 or ey > y-15:
                    #print("can stretch vertically")
                    self.isStretchingV = True
        event.ignore()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self,event):
        #print("mouse release event on tile at x: {} y: {}".format(event.x(),event.y()))
        ex = event.pos().x()
        ey = event.pos().y()
        x = self.size().width()
        y = self.size().height()
        size = QSize()
        
        if self.isStretchingH:
            if self.mousePosn.x() < x-15:
                if ex < x:
                    size.setWidth(x-ex)
            else:
                if ex > 0:
                    size.setWidth(ex)
        else:
            size.setWidth(x)
        if self.isStretchingV:
            if self.mousePosn.y() < y-15:
                if ey < y:
                    size.setHeight(y-ey)
            else:
                if ey > 0:
                    size.setHeight(ey)
        else:
            size.setHeight(y)

        if self.isStretchingH or self.isStretchingV:
            #print("cur size: {} resize: {}".format(self.size(),size))
            #self.resize(size)
            self.setPixmap(self.pixmap().scaled(size,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
            #print(self.pixmap().size())
            #print(QRect(self.pos(),size))
            self.setGeometry(QRect(self.pos(),size))
            #print("cur size after resizing?: {}".format(self.size()))
            self.isStretchingH = False
            self.isStretchingV = False
            

    def mouseMoveEvent(self,event):
        if self.isMouseDown and not self.isStretchingH and not self.isStretchingV:
            time = self.mouseTime.elapsed()
            dist = (event.pos() - self.mousePosn).manhattanLength()
            if time >= QApplication.startDragTime() or dist >= QApplication.startDragDistance():
                if self.canCopy:
                    self.execDragging(Qt.CopyAction)
                if self.canMove:
                    self.execDragging(Qt.MoveAction)
                self.isMouseDown = False
                event.accept()
                return
        event.ignore()
        super().mouseMoveEvent(event)
        
    def execDragging(self,actions):
        drag = QDrag(self)
        ghost = self.grab().scaledToHeight(50)
        drag.setPixmap(ghost)
        drag.setHotSpot(QPoint(ghost.width()/2,ghost.height()/2))
        mdata = QMimeData()
        mdata.setImageData(self.pixmap())
        mdata.setText(self.name)
        drag.setMimeData(mdata)

        act = drag.exec_(actions)
        defact = drag.defaultAction()
        targ = drag.target()
        src = drag.source()
        #self.debug(act,defact,targ,src)
        return targ is not self.parentWidget()

    def debug(self,act,defact,targ,src):
        print('exec returns {} default {} target {} source {}'.format(int(act),int(defact),type(targ),type(src)))



'''
import unittest

class Tester(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile("space.jpeg")
        self.tile2 = Tile("space.jpeg")
        self.tile3 = Tile("space2.jpeg")
        
    def test_equal(self):
        self.assertEqual(self.tile1,self.tile2)

    def test_notEqual(self):
        self.assertNotEqual(self.tile1,self.tile3)

if __name__ == '__main__':
    unittest.main()
'''
