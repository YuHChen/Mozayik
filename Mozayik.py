from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Viewer import *
from Canvas import *

import os

class Mozayik(QWidget):
    def __init__(self, parent=None):
        super(Mozayik, self).__init__(parent)

        mainLayout = QHBoxLayout()
        
        #setup button icons
        assets = os.getcwd() + "/assets"
        if os.path.exists(assets):
            os.chdir(assets)
            trash = assets + "/trash.png"
            if os.path.isfile(trash):
                trashIcon = QIcon(QPixmap(trash))
            add = assets + "/plus.png"
            if os.path.isfile(add):
                addIcon = QIcon(QPixmap(add))
            folder = assets + "/folder.png"
            if os.path.isfile(folder):
                folderIcon = QIcon(QPixmap(folder))

        #setup buttons
        self.enterFolderButton = QPushButton(folderIcon, "")
        self.enterFolderButton.clicked.connect(self.enterFolderContact)
        self.addTilesButton = QPushButton(addIcon, "")
        self.addTilesButton.clicked.connect(self.addTilesContact)
        self.deleteButton = QPushButton(trashIcon, "")
        self.deleteButton.clicked.connect(self.deleteContact)

        #layout buttons
        buttonLayout1 = QHBoxLayout()
        buttonLayout1.addWidget(self.enterFolderButton)
        buttonLayout1.addWidget(self.addTilesButton)
        buttonLayout1.addWidget(self.deleteButton)

        #setup image viewer
        scrollView = QScrollArea()
        scrollView.setBackgroundRole(QPalette.Dark)
        self.viewer = Viewer()
        scrollView.setWidget(self.viewer)
        size = QSize(350,600)
        scrollView.setMaximumSize(size)
        #scrollView.setMinimumSize(size)

        #setup mozayik area
        #self.mozayik = QLabel("Area reserved")
        self.mozayik = Canvas()

        #layout main view
        viewLayout1 = QVBoxLayout()
        viewLayout1.addLayout(buttonLayout1)
        viewLayout1.setAlignment(buttonLayout1,Qt.AlignRight)
        viewLayout1.addWidget(scrollView)
        viewLayout1.setAlignment(scrollView,Qt.AlignLeft)
        
        mainLayout.addLayout(viewLayout1)
        mainLayout.addWidget(self.mozayik)

        self.setLayout(mainLayout)
        self.setWindowTitle("Mozayik")

        #print("mozayik size:")
        #print(self.size())

    def enterFolderContact(self):
        self.viewer.openFolder()
    
    def addTilesContact(self):
        self.viewer.addTiles()

    def deleteContact(self):
        self.mozayik.delete()

    def sizeHint(self):
        return self.minimumSize()
        
    def minimumSize(self):
        size = QSize(16,9)
        size.scale(700,700,Qt.KeepAspectRatioByExpanding)
        #print("size hint for mozayik")
        #print(size)
        return size

if __name__ == '__main__':    
    app = QApplication(sys.argv)

    screen = Mozayik()
    screen.show()
    
    sys.exit(app.exec_())

