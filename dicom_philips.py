# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:46:11 2014

@author: jeff
"""
import dicom, sys, os, shutil, glob
from PySide.QtCore import *
from PySide.QtGui import *
#from mvpa2.suite import *
import nibabel as nib
#from mvpa2.suite import fmri_dataset, SampleAttributes

"""TODO: Need to create loop for slope eval over multivolume series
Check for multivol then perform loop
DONE: If completion, move to Processed folder (may have been done)
DONE: Remove 0:5 condition on main loop
Assumption: Scale on all multivolume images is the same
May want to output a text file of subjid and dicom_name completed + errors"""


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

def folder_process_dicoms():
    """Select the data using a PYQT window, then loop over a dicom conversion and fix"""      
    dataset_folder= get_folder()    
    files = os.listdir(dataset_folder)

    ## Create folders if they do not exist
    temp_folder=os.path.join(dataset_folder, 'Temp')
    output_folder=os.path.join(dataset_folder, 'Processed')
    error_folder=os.path.join(dataset_folder, 'Errors')
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder); print "Made Temp Folder"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder); print "Made Processed Folder"
    if not os.path.exists(error_folder):
        os.mkdir(error_folder); print "Made Errors Folder"    

    ## Main Loop for converting and fixing Dicoms (i is a single Dicom file)    
    for i in files: #[1:2]:
        dataset=os.path.join(dataset_folder,i)      
        try:
            convert_dicom(dataset, temp_folder)
            correct_dicom(dataset, temp_folder, output_folder)
            flush_temp_folder(temp_folder, error_folder)
            print "Dicom Converted and Corrected Successfully:\t ", i
        except:
            print "Error in Dicom Process!!: \t ", i
            move_to_error_folder(temp_folder, error_folder)
 
def convert_dicom(dicom_file, output_folder):
    """Use mcverter (from MRIConvert) to convert Dicom >> Nifti"""    
    mcverter_input="mcverter -o {0} -f {1}  -d -n -u -q -F -PatientName,+PatientId,-SeriesDate,-SeriesTime,-StudyId,-StudyDescription,+SeriesNumber,-SequenceName,+ProtocolName,-SeriesDescription {2}".format(output_folder, 'fsl', dicom_file)      
    #mcverter_input="mcverter -o {0} -f {1} -j -d  -n -u -F PatientID {2}".format(output_folder, 'fsl', dicom_file)      
    #mcverter_input="mcverter -o {0} -f {1} -d -u -n {2} -F -SeriesDate,-SeriesTime,-SeriesDescription,-StudyID,-SeriesNumber,-SequenceName ".format(output_folder, 'fsl', dicom_file)
    os.system(mcverter_input)
    
    
def correct_dicom(dicom_file, temp_nifti_folder, processed_folder):
    """Divide the dicom image by the scale factor found in the Dicom"""
    if not os.listdir(temp_nifti_folder):
        return Exception
    ds=dicom.read_file(dicom_file)
    
    ## Get Scale from Dicom Header     
    try:
        slope=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1053].value
        intercept=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1052].value
        scale_type=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1054].value
    except:
        try:
            slope=ds[0x0028,0x1053].value
            intercept=ds[0x0028,0x1052].value
            scale_type=ds[0x0028,0x1054].value
        except:
            return Exception
            
    ## Filter and load nifti file
    list_of_niftis = glob.fnmatch.filter(os.listdir(temp_nifti_folder),'*.nii')
    
    ## Load Nifti File and Correct Nifti File for curr_nifti_file in list_of_niftis: img=nib.load(curr_nifti_file)        
    while list_of_niftis!=[]:   
        try:        
            curr_nifti_file=list_of_niftis.pop()        
            img=nib.load(os.path.join(temp_nifti_folder,curr_nifti_file)) 
            hdr=img.get_header()
            pix_nifti=img.get_data()
            pix_corrected=pix_nifti/float(slope)#### Major Component of Analysis
            output_nifti_name=curr_nifti_file.split(".")[0] + "_Corrected." + curr_nifti_file.split(".")[-1]
            #hdr.data_to_fileobj(pix_corrected, './'+output_nifti_name.__str__())
            img2=nib.Nifti1Image(pix_corrected,img.get_affine(), header=hdr)
            img2.to_filename(os.path.join(processed_folder,output_nifti_name))
            #os.remove(os.path.join(temp_nifti_folder,curr_nifti_file))
        except:
            return Exception
                       
def flush_temp_folder(temp_folder, error_folder):
    if os.listdir(temp_folder) != []:
        for filename in os.listdir(temp_folder):
            shutil.move(os.path.join(temp_folder, filename), error_folder)
        
def move_to_error_folder(temp_folder, error_folder):
    temp_contents=[os.path.join(temp_folder,i) for i in os.listdir(temp_folder)]
    [shutil.move(file, error_folder) for file in temp_contents]
  
if __name__ == "__main__":
    """Runs the main loop for import.  If prompt=True, then user inputs will be given, otherwise it will autoload TBSS_Data3"""
    #output_dataset = main(prompt = True)
    output_dataset = folder_process_dicoms()


