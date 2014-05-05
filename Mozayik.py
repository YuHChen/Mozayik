from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Viewer import *
from Canvas import *

class Mozayik(QWidget):
    def __init__(self, parent=None):
        super(Mozayik, self).__init__(parent)

        mainLayout = QHBoxLayout()

        #setup buttons
        self.enterFolderButton = QPushButton("   Choose folder   ")
        self.enterFolderButton.clicked.connect(self.enterFolderContact)
        self.addTilesButton = QPushButton("   Add Tiles   ")
        self.addTilesButton.clicked.connect(self.addTilesContact)
       
        #layout buttons
        buttonLayout1 = QHBoxLayout()
        buttonLayout1.addWidget(self.enterFolderButton)
        buttonLayout1.addWidget(self.addTilesButton)

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

    def sizeHint(self):
        return self.minimumSize()
        
    def minimumSize(self):
        size = QSize(16,9)
        size.scale(700,700,Qt.KeepAspectRatioByExpanding)
        print("size hint for mozayik")
        print(size)
        return size

if __name__ == '__main__':    
    app = QApplication(sys.argv)

    screen = Mozayik()
    screen.show()
    
    sys.exit(app.exec_())

