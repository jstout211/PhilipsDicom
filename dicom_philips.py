# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:46:11 2014

@author: jeff
"""
import dicom, sys, os
from PySide.QtCore import *
from PySide.QtGui import *
#from mvpa2.suite import fmri_dataset, SampleAttributes

os.chdir('/media/3T_Data1/MRI_ARCHIVE/20')
inputs=os.listdir('.')

#%% Folder Get
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

def folder_process_dicoms():
    """Select the data using a PYQT window, then loop over a dicom conversion and fix"""      
    dataset_folder= get_folder()    
    files = os.listdir(dataset_folder)

def temp_proc():
    for i in files[0:10]:
        dataset=os.path.join(dataset_folder,i)
        output_folder=os.path.join(dataset_folder, 'Processed')        
        try:
            convert_dicom(dataset, output_folder)
            print "Dicom Converted Successfully:\t ", i
        except:
            print "Error in Dicom Process!!: \t ", i
#            move_nifti()
#            print "Moving to output folder"        
        
#            move_dicom_fail()
    #dataset = glob.fnmatch.filter(os.listdir(dataset_folder), '*.nii*')
    #dat= [g for i in dataset: g = dataset_folder + i]
    
    
def convert_dicom(dicom_file, output_folder):
    """Use mcverter (from MRIConvert) to convert Dicom >> Nifti"""
    mcverter_input="mcverter -o {0} -f {1} -j -d  -n -u -F -PatientName, PatientId, SeriesDate, SeriesTime, StudyId, StudyDescription, SeriesNumber, SequenceName, ProtocolName, SeriesDescription {2}".format(output_folder, 'fsl', dicom_file)      
    #mcverter_input="mcverter -o {0} -f {1} -j -d  -n -u -F PatientID {2}".format(output_folder, 'fsl', dicom_file)      
    #mcverter_input="mcverter -o {0} -f {1} -d -u -n {2} -F -SeriesDate,-SeriesTime,-SeriesDescription,-StudyID,-SeriesNumber,-SequenceName ".format(output_folder, 'fsl', dicom_file)
    os.system(mcverter_input)
    


        try:
            print "Dicom: ", i, " Converted successfully"
        except:
            pass











#tempvar={}
#for i,j in enumerate(inputs):
#    try:    
#        ds=dicom.read_file(inputs[i])
#        pix=ds.pixel_array
#        if pix.shape[0] > 10:
#            tempvar[i]=inputs[i]            
#            #tempvar.append(inputs[i])
#    except:
#        print "Cant process ", inputs[i]
#        
#for i,z in enumerate(inputs):
#    print i
#    
    
    
#%%         Find TFE SENSE
tempvar={}
prot_name={}
for i,j in enumerate(inputs[0:100]):
    try:    
        ds=dicom.read_file(inputs[i])
        prot_name[i]=ds[0x0018,0x1030].value
        #pix=ds.pixel_array
        #if pix.shape[0] > 10:
        #    tempvar[i]=inputs[i]            
            #tempvar.append(inputs[i])
    except:
        print "Cant process ", inputs[i]
        
for i,z in enumerate(inputs):
    print i, prot_name[i]
      
    
    
    
    
#rescale_intercept=ds[0x0028,0x1052]    
#rescale_slope=ds[0x0028,0x1053] 

output={}
maxoutput={}
for i,j in  enumerate(tempvar.keys()): #enumerate(tempvar):
    #print j
    ds=dicom.read_file(tempvar[j])
    try:
        slope=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1053].value
        intercept=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1052].value
        scale_type=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1054].value
        output[i]=[slope,intercept,scale_type]
    except:
        try:
            slope=ds[0x0028,0x1053].value
            intercept=ds[0x0028,0x1052].value
            scale_type=ds[0x0028,0x1054].value
            output[i]=[slope,intercept,scale_type]
        except:
            output[i]=["noval","noval"]            
    #dim=pix.shape[0]/2    
    #imshow(pix[dim,:,:]) 
    try: 
        pix=ds.pixel_array
        maxoutput[i]=pix.max()
    except:
        pass
    
for i in range(len(output)):
    if output[i][0] != 'noval':
        #print output[i], maxoutput[i]
        print i, output[i][0], maxoutput[i]/output[i][0]
    

ds=dicom.read_file(inputs[4])


#%%    
imshow(pix[45,:,:]) 
np.max(np.max(np.max(pix))) 


slope=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1053].value
intercept=ds.PerframeFunctionalGroups[0][0x2005,0x140f][0][0x0028,0x1052].value

#%%
import dicom
from mvpa2.suite import *
import nibabel as nib
os.chdir('/home/jeff/Desktop/TempTempFile/TestFixed')


ds=dicom.read_file('IM_0005')
pix=ds.pixel_array

img=nib.load('./Test.nii')

hdr=img.get_header()
hdr.data_to_fileobj(pix,img)
pix2=pix.swapaxes(0,2)

#%%
   
if __name__ == "__main__":
    """Runs the main loop for import.  If prompt=True, then user inputs will be given, otherwise it will autoload TBSS_Data3"""
    #output_dataset = main(prompt = True)
    output_dataset = folder_process_dicoms()











