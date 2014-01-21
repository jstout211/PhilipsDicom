# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:46:11 2014

@author: jeff
"""
import dicom
os.chdir('/media/3T_Data1/MRI_ARCHIVE/20')

inputs=os.listdir('.')


tempvar={}
for i,j in enumerate(inputs):
    try:    
        ds=dicom.read_file(inputs[i])
        pix=ds.pixel_array
        if pix.shape[0] > 10:
            tempvar[i]=inputs[i]            
            #tempvar.append(inputs[i])
    except:
        print "Cant process ", inputs[i]
        
for i,z in enumerate(inputs):
    print i
    
    
    
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

######################################################   COMPARE OSIRIX VERSUS PYDICOM SLOPE TAGS

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


=











