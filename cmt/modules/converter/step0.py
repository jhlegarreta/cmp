import os, os.path as op
import logging
log = logging.getLogger()
from glob import glob
import subprocess
import sys
import shutil

import nibabel.nicom.dicomreaders as dr
import nibabel as ni

def diff2nifti_diff_unpack():

    raw_dir = op.join(gconf.get_raw4subject(sid))
    
    nifti_dir = op.join(gconf.get_nifti4subject(sid))
    if not op.exists(nifti_dir):
        try:
            os.makedirs(nifti_dir)
        except os.error:
            log.info("%s was already existing" % str(nifti_dir))
    
    
    if gconf.processing_mode == 'DSI':
        dsi_dir = op.join(raw_dir, 'DSI')
        log.info("Convert DSI ...") 
        # check if .nii / .nii.gz is already available
        if op.exists(op.join(dsi_dir, 'DSI.nii')):
            shutil.copy(op.join(dsi_dir, 'DSI.nii'), op.join(nifti_dir, 'DSI.nii'))
        else:
            # read data
            from glob import glob
            first = sorted(glob(op.join(dsi_dir, gconf.raw_glob)))[0]
            diff_cmd = 'diff_unpack %s %s' % (first, op.join(nifti_dir, 'DSI.nii'))
            
            subprocess.call(diff_cmd, shell=True)
    
        log.info("Resampling 'DSI' to 1x1x1 mm^3...")
    
        mri_cmd = 'mri_convert -vs 1 1 1 %s %s' % (
                               op.join(nifti_dir, 'DSI.nii'),
                               op.join(nifti_dir, 'DSI_b0_resampled.nii'))
        
        subprocess.call(mri_cmd, shell=True)

def diff2nifti():
    
    raw_dir = op.join(gconf.get_raw4subject(sid))
    
    nifti_dir = op.join(gconf.get_nifti4subject(sid))
    if not op.exists(nifti_dir):
        try:
            os.makedirs(nifti_dir)
        except os.error:
            log.info("%s was already existing" % str(nifti_dir))
    
    
    if gconf.processing_mode == 'DSI':
        dsi_dir = op.join(raw_dir, 'DSI')
        log.info("Convert DSI ...") 
        # check if .nii / .nii.gz is already available
        if op.exists(op.join(dsi_dir, 'DSI.nii')):
            shutil.copy(op.join(dsi_dir, 'DSI.nii'), op.join(nifti_dir, 'DSI.nii'))
        else:
            # read data
            dd = dr.read_mosaic_dir(dsi_dir, gconf.raw_glob)
            # save data and affine as nifti
            ni.save(ni.Nifti1Image(dd[0], dd[1]), op.join(nifti_dir, 'DSI.nii'))
            log.info("Dataset 'DSI.nii' successfully created!")
    
        log.info("Resampling 'DSI' to 1x1x1 mm^3...")
    
        mri_cmd = 'mri_convert -vs 1 1 1 %s %s' % (
                               op.join(nifti_dir, 'DSI.nii'),
                               op.join(nifti_dir, 'DSI_b0_resampled.nii'))

# XXX: does not create resampled. nii
#MRIalloc(212, 212, 126): could not allocate 89888 bytes for 30142th slice
#Cannot allocate memory
# ALSO NOT WITH diff_unpack
        
        log.info("Starting mri_convert ...")
        proc = subprocess.Popen(mri_cmd,
                               shell = True,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               cwd = gconf.get_cmt_rawdiff4subject(sid))
        
        out, err = proc.communicate()
        log.info(out)
        
    elif gconf.processing_mode == 'DTI':
        dsi_dir = op.join(raw_dir, 'DSI')
        log.info("Convert DTI ...") 
        # check if .nii / .nii.gz is already available
        if op.exists(op.join(dsi_dir, 'DTI.nii')):
            shutil.copy(op.join(dsi_dir, 'DTI.nii'), op.join(nifti_dir, 'DTI.nii'))
        else:
            # read data
            dd = dr.read_mosaic_dir(dsi_dir, gconf.raw_glob)
            # save data and affine as nifti
            ni.save(ni.Nifti1Image(dd[0], dd[1]), op.join(nifti_dir, 'DTI.nii'))
            log.info("Dataset 'DTI.nii' successfully created!")
    
        log.info("Resampling 'DTI' to 1x1x1 mm^3...")
    
        mri_cmd = ['mri_convert -vs 1 1 1 %s %s' % (
                               op.join(nifti_dir, 'DTI.nii'),
                               op.join(nifti_dir, 'DTI_b0_resampled.nii.gz'))]
    
        
        # XXX: does not create resampled. nii
        log.info("Starting mri_convert ...")
        proc = subprocess.Popen(' '.join(mri_cmd),
                               shell = True,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               cwd = gconf.get_cmt_rawdiff4subject(sid))
        
        out, err = proc.communicate()
        log.info(out)
        
        

def t12nifti():
    
    raw_dir = op.join(gconf.get_raw4subject(sid))
    nifti_dir = op.join(gconf.get_nifti4subject(sid))
    
    log.info("Converting 'T1'...")
    t1_dir = op.join(raw_dir, 'T1')
    # check if .nii / .nii.gz is already available
    if op.exists(op.join(t1_dir, 'T1.nii')):
        shutil.copy(op.join(t1_dir, 'T1.nii'), op.join(nifti_dir, 'T1.nii'))
    else:
        
        # read data
        dd = dr.read_mosaic_dir(t1_dir, gconf.raw_glob)

        ## change orientation of "T1" to fit "b0"
        #"${CMT_HOME}/registration"/nifti_reorient_like.sh "T1.nii" "DSI.nii"

        # save data and affine as nifti
        ni.save(ni.Nifti1Image(dd[0], dd[1]), op.join(nifti_dir, 'T1.nii'))
    
        log.info("Dataset 'T1.nii' succesfully created!")
        
def t12nifti_diff_unpack():

    raw_dir = op.join(gconf.get_raw4subject(sid))
    nifti_dir = op.join(gconf.get_nifti4subject(sid))
    
    log.info("Converting 'T1'...")
    t1_dir = op.join(raw_dir, 'T1')
    if op.exists(op.join(t1_dir, 'T1.nii')):
        shutil.copy(op.join(t1_dir, 'T1.nii'), op.join(nifti_dir, 'T1.nii'))
    else:
        from glob import glob
        first = sorted(glob(op.join(t1_dir, gconf.raw_glob)))[0]
        diff_cmd = 'diff_unpack %s %s' % (first, op.join(nifti_dir, 'T1.nii'))
        
        subprocess.call(diff_cmd, shell=True)
        
def t22nifti():
    
    raw_dir = op.join(gconf.get_raw4subject(sid))
    nifti_dir = op.join(gconf.get_nifti4subject(sid))
    
    log.info("Converting 'T2'...")
    t2_dir = op.join(raw_dir, 'T1')
    # check if .nii / .nii.gz is already available
    if op.exists(op.join(t2_dir, 'T2.nii')):
        shutil.copy(op.join(t2_dir, 'T2.nii'), op.join(nifti_dir, 'T2.nii'))
    else:
        
        # read data
        dd = dr.read_mosaic_dir(t2_dir, gconf.raw_glob)

        #    # change orientation of "T2" to fit "b0"
        #    "${CMT_HOME}/registration"/nifti_reorient_like.sh "T2.nii" "DSI.nii"

        # save data and affine as nifti
        ni.save(ni.Nifti1Image(dd[0], dd[1]), op.join(nifti_dir, 'T2.nii'))
    
        log.info("Dataset 'T2.nii' successfully created!")

    log.info("[ DONE ]")
    


def run(conf, subject_tuple):
    """ Run the first dicom converter step
    
    Parameters
    ----------
    conf : PipelineConfiguration object
    subject_tuple : tuple, (subject_id, timepoint)
        Process the given subject
        
    """
    # setting the global configuration variable
    globals()['gconf'] = conf
    globals()['sid'] = subject_tuple
    
    log.info("DICOM -> NIFTI conversion")
    log.info("=========================")
    
    diff2nifti_diff_unpack()
    #t12nifti_diff_unpack()
    
#    diff2nifti()
#    t12nifti()
#    if gconf.registration_mode == 'N':
#        t22nifti()
#    
    