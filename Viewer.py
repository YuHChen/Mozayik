from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os,sys,glob

from Tile import *

class Viewer(QWidget):
    def __init__(self, parent=None):
        super(Viewer, self).__init__(parent)

        self.tileList = []

        #self.setMinimumSize(QSize(300,300))

        os.chdir("{}/Pictures".format(os.environ['HOME']))
        mainLayout = self.makePicLayout(self.getPicList())
        self.setLayout(mainLayout)
        
    def sizeHint(self):
        size = QSize(300, 200*len(self.tileList))
        return size

    #grab images with jpg, jpeg, and png extenstions
    def getPicList(self):
        jpgs = glob.glob("*.jpg")
        jpegs = glob.glob("*.jpeg")
        pngs = glob.glob("*.png")
        picList = jpgs + jpegs + pngs
        return picList

    #create layout with the list of images
    #no repeating images
    def makePicLayout(self, picList):
        picLayout = QVBoxLayout()
        for pic in picList:
            tile = Tile(pic)
            if tile not in self.tileList:
                tile.setCanCopy(True)
                self.tileList.append(tile)
        for tile in self.tileList:
            picLayout.addWidget(tile)
        return picLayout

    #set view to show images in choosen folder
    def openFolder(self,folderPath=None):
        if(folderPath is None):
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
            dialog.setViewMode(QFileDialog.Detail)
            dialog.setDirectory("{}".format(os.environ['HOME']))
            if(dialog.exec()):
                folderPath = str(dialog.selectedFiles()[0])
            else:
                folderPath = ""
                if folderPath == "":
                    #QMessageBox.information(self, "Error", "No folder path received.")
                    return
        
        os.chdir(folderPath)
        picList = self.getPicList()
        
        for tile in self.tileList:
            tile.deleteLater()
        self.tileList = []
        picLayout = self.makePicLayout(picList)
        self.layout().removeItem(self.layout())
        self.setLayout(picLayout)
        self.adjustSize()
        
    #add selected images to view
    def addTiles(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg *jpeg)")
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory("{}".format(os.environ['HOME']))
        if(dialog.exec()):
            tilePaths = dialog.selectedFiles()
        else:
            tilePaths = ""
        if tilePaths == "":
            #QMessageBox.information(self, "Error", "No images selected.")
            return

        folder = os.path.commonprefix(tilePaths)
        while(not os.path.isdir(folder)):
            folder = os.path.dirname(folder)
        os.chdir(folder)
        tileNames = [os.path.basename(path) for path in tilePaths]
        print(tileNames)
        picLayout = self.makePicLayout(tileNames)
        self.layout().removeItem(self.layout())
        self.setLayout(picLayout)
        self.adjustSize()
        
