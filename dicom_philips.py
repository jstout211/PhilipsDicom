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
If completion, move to Processed folder (may have been done)
Remove 0:5 condition on main loop"""




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
    for i in files[0:5]:
        dataset=os.path.join(dataset_folder,i)      
        try:
            convert_dicom(dataset, temp_folder)
            correct_dicom(dataset, temp_folder, output_folder)
            print "Dicom Converted Successfully:\t ", i
        except:
            print "Error in Dicom Process!!: \t ", i
            move_to_error_folder(temp_folder, error_folder)
     
        
#            move_dicom_fail()
    #dataset = glob.fnmatch.filter(os.listdir(dataset_folder), '*.nii*')
    #dat= [g for i in dataset: g = dataset_folder + i]
    
    
def convert_dicom(dicom_file, output_folder):
    """Use mcverter (from MRIConvert) to convert Dicom >> Nifti"""    
    mcverter_input="mcverter -o {0} -f {1}   -n -u -q -F -PatientName,+PatientId,-SeriesDate,-SeriesTime,-StudyId,-StudyDescription,+SeriesNumber,-SequenceName,+ProtocolName,-SeriesDescription {2}".format(output_folder, 'fsl', dicom_file)      
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
        except:
            return Exception
                
        
def scale_niftis(scale, nifti_data):
    """        """

    
        
def move_to_error_folder(temp_folder, error_folder):
    temp_contents=test=[os.path.join(temp_folder,i) for i in os.listdir(temp_folder)]
    [shutil.move(file, error_folder) for file in temp_contents]



folder_process_dicoms()
    







#%%  REMVOE ALL OF BELOW
from mvpa2.suite import *
import nibabel as nib
os.chdir('/home/jeff/Desktop/TempTempFile/TestFixed')


ds=dicom.read_file('IM_0005')
pix=ds.pixel_array

img=nib.load('./Test.nii')

hdr=img.get_header()
hdr.data_to_fileobj(pix,img)
pix2=pix.swapaxes(0,2)









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











