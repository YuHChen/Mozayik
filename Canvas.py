from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os,sys,glob

from Tile import *
from CanvasLayout import *

def translate_actions(actions):
    msg = 'actions:'
    if actions & Qt.CopyAction : msg += ' Copy'
    if actions & Qt.MoveAction : msg += ' Move'
    if actions & Qt.LinkAction : msg += ' Link'
    return msg

class Canvas(QWidget):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setAcceptDrops(True)

        self.setLayout(CanvasLayout(self,11,5,5))

        self.tileList = []
        self.curTile = None

        self.movePoint = QPoint(-1,-1)

    def delete(self):
        if self.curTile is not None:
            self.layout().delete(self.curTile)
            if self.tileList.count(self.curTile) == 1:
                self.tileList.remove(self.curTile)
            else:
                for i in range(0, len(self.tileList)):
                    if id(self.tileList[i]) == id(self.curTile):
                        self.tileList[i].close()
                        self.tileList.pop(i)
                        break
            self.layout().activate()
            self.curTile = None

    def sizeHint(self):
        return self.maximumSize()

    def maximumSize(self):
        size = QSize(self.parentWidget().size().width()-self.parentWidget().viewer.size().width(), self.parentWidget().size().height())
        return size

    def mousePressEvent(self, event):
        #print("mouse click on canvas")
        #print("canvas size: {}".format(self.size()))
        for tile in self.tileList:
            if tile.underMouse():
                self.curTile = tile
        
    def mouseReleaseEvent(self, event):
        #print("mouse release event on canvas")
        pass
        
    def dragEnterEvent(self, event):
        actions = event.possibleActions()
        self.movePoint = event.pos()
        #msg1 = 'drag enters at {0} {1}'.format(event.pos().x(), event.pos().y())
        #msg2 = 'kbd mods {0:0x} buttons {1:0x}'.format(int(event.keyboardModifiers()),int(event.mouseButtons()))
        #print(msg1, msg2, 'offering',translate_actions(actions))
        if (event.mimeData().hasImage()):
            if actions & Qt.CopyAction :
                event.acceptProposedAction()
            else:
                #print('setting copy action')
                event.setDropAction(Qt.CopyAction)
                event.accept()

    #def dragMoveEvent(self, event):
    #    pass

    def dropEvent(self, event):
        #print("drop event occurred")
        #msg = 'dropping at {0} {1}'.format(event.pos().x(), event.pos().y())
        actions = event.dropAction()
        #print(msg,translate_actions(actions))
        if actions & Qt.CopyAction:
            event.acceptProposedAction()
            if (event.mimeData().hasImage() and event.mimeData().hasText()):
                pixmap = QPixmap(event.mimeData().imageData())
                name = event.mimeData().text()
                tile = Tile(name,pixmap)
                tile.setCanMove(True)
                tile.setCanStretch(True)
                self.tileList.append(tile)
                self.layout().addWidget(tile)
                event.accept()
        elif actions & Qt.MoveAction:
            #print("move tile")
            targ = self.layout().itemAtPos(event.pos())
            if targ is not None:
                self.layout().swapWidgets(self.curTile, targ)
                event.acceptProposedAction()
        else:
            event.ignore()
