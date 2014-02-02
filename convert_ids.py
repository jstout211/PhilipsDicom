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
    """During Initialization it creates a dictionary of medical ID keys 
    with MEGID values"""     
    def __init__(self):
        self.files=[]
        self.medid_dict=self.create_medid_dictionary()
        
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
            tbis=[]
            non_tbis=[]
            #print 'Current: ', i    
            output=re.search(patfinder,filename)
            if output != None:
                med_id=output.group()
                meg_id=self.convert_name(filename, med_id)
                if meg_id == "NOT_TBI":
                    non_tbis.append(filename)
                else:
                    tbis.append(meg_id+filename[output.end():])
                    print med_id, meg_id+filename[output.end():], self.return_scan_type(filename)                  
                
                
    def convert_name(self,filename, med_id):
        """Input MedId and outputs MEG_ID >> else returns NOT_TBI"""        
        try:
            return self.medid_dict[med_id][1]
        except:
            return "NOT_TBI"

    def create_medid_dictionary(self):
        medid_dict={}
        import csv
        with open('/media/Data_3T_D1/Functions/PhilipsDicom/PhilipsDicom/MedID_List.csv','rb') as csvfile:
            reader=csv.reader(csvfile)
            for row in reader:
                medid_dict[row[3]]=row[0:4]
        return medid_dict
        
    def return_scan_type(self,filename):
        if re.search('DTI',filename):
            return 'DTI'
        elif re.search('3D_TFE_SENSE', filename):
            return 'T1'
        elif re.search('fMRI_VERB_GENERATION', filename):
            return 'VERB_GEN'
        elif re.search('fMRI_WORD_GENERATION_SENSE', filename):
            return 'WORD_GEN'            
        elif re.search('252_fMRI_FLANKER_ARROW_SENSE', filename):
            return 'FLANKER_ARROW'  
        elif re.search('Resting_fMRI_FLANKER_ARROW_SENSE', filename):
            return 'REST' 
        elif re.search('fMRI_N-BACK_SENSE', filename):
            return 'NBACK'
        elif re.search('FLAIR_AXIAL__T2W_FLAIR', filename):
            return 'FLAIR'            
        else:
            return filename

        

        

        
        
            
            

        




