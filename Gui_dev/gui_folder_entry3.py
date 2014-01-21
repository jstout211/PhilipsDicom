# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:49:18 2013

@author: brain
"""
import sys
from PySide.QtCore import *
from PySide.QtGui import *

def get_folder():
    try:
        dialog = QApplication([])
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
    except RuntimeError:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        #dialog = QCoreApplication.instance()
    dialog.exec_()
    filename=dialog.selectedFiles()[0]
    return filename


#app.exit()
            
        
