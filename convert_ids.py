# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:29:05 2014

@author: jeff
"""

import re
import sys, os, shutil, glob
from PySide.QtCore import *
from PySide.QtGui import *
#

def get_folder():
    """Retrieve Folder using QT file browser"""    
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


def identify_medid(files):
    pattern = 'M\d{9,12}'
    patfinder=re.compile(pattern)        
    
    for i in files:
        output=[]
        #print 'Current: ', i    
        output=re.search(patfinder,i)
        if output != None:
            print output.group()
            
            

        




