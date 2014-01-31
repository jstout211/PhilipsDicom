# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:29:05 2014

@author: jeff
"""

import re
import sys, os, shutil, glob
from PySide.QtCore import *
from PySide.QtGui import *
import pickle

class FileConvert:
    def __init__(self):
        self.files=[]
        
    def _get_folder(self):
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
    
    
    def identify_medid(self): #  files, tbi_med_ids):
        """Uses Gui to identify folder and pull list of files.  
        This performs a template match to a medical ID number M"9-12 digits"
        This then calls a dictionary to lookup the MEGSubjectID"""
        files=os.listdir(self._get_folder())    
        pattern = 'M\d{9,12}'
        patfinder=re.compile(pattern) 
        for filename in files:
            output=[]
            med_id=[]
            #print 'Current: ', i    
            output=re.search(patfinder,filename)
            if output != None:
                med_id=output.group()
                self.convert_name(filename, med_id)
                
                
    def convert_name(self,filename, med_id):
        print filename, med_id
        os.
        
            
            

        




