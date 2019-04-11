import os
os.environ['SUBJECTS_DIR'] = '/Users/admin/Dropbox (Weizmann Institute)/tunnel/freesurfer_subjects'
from mayavi import mlab

fig = mlab.figure(size=(1000,550))

mlab.savefig('test_fmri_activation.png',figure=fig,magnification=5) # save a high-res figure