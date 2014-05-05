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

        self.setLayout(CanvasLayout())

        self.tileList = []

        self.movePoint = QPoint(-1,-1)

    def sizeHint(self):
        size = QSize(self.parentWidget().size().width()-self.parentWidget().viewer.size().width(), self.parentWidget().size().height())
        self.setMaximumSize(size)
        return size

    def mousePressEvent(self, event):
        print("mouse click on canvas")
        print("canvas size: {}".format(self.size()))
        
    def mouseReleaseEvent(self, event):
        print("mouse release event on canvas")

    def dragEnterEvent(self, event):
        actions = event.possibleActions()
        self.movePoint = event.pos()
        msg1 = 'drag enters at {0} {1}'.format(event.pos().x(), event.pos().y())
        msg2 = 'kbd mods {0:0x} buttons {1:0x}'.format(int(event.keyboardModifiers()),int(event.mouseButtons()))
        print(msg1, msg2, 'offering',translate_actions(actions))
        if (event.mimeData().hasImage()):
            if actions & Qt.CopyAction :
                event.acceptProposedAction()
            else:
                print('setting copy action')
                event.setDropAction(Qt.CopyAction)
                event.accept()

    #def dragMoveEvent(self, event):
    #    pass

    def dropEvent(self, event):
        print("drop event occurred")
        msg = 'dropping at {0} {1}'.format(event.pos().x(), event.pos().y())
        actions = event.dropAction()
        print(msg,translate_actions(actions))
        if actions & Qt.CopyAction:
            event.acceptProposedAction()
        #else:
            #print("setting copy action!")
            #event.setDropAction(Qt.CopyAction)
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
            print("move tile")
            event.acceptProposedAction()
            
        else:
            event.ignore()
