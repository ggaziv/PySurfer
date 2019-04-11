#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flat patch demo.
"""

from surfer import Brain
from mayavi import mlab
import os, nibabel as nib, numpy as np
os.environ['SUBJECTS_DIR'] = '/Users/admin/Dropbox (Weizmann Institute)/tunnel/freesurfer_subjects'
cortical_maps_path = '/Users/admin/Dropbox (Weizmann Institute)/tunnel/cortical_maps'
print(__doc__)

fig = mlab.figure(size=(1000,550))

# brain = Brain("fsaverage", "both", "cortex.patch.flat",
#               subjects_dir='/usr/local/freesurfer/subjects',
#               figure=fig,background='w')
# brain = Brain("fsaverage", "both", "cortex.patch.flat",
#               figure=fig,background='w')
# brain = Brain("Kamitani_sbj3", "both", "full.flat.patch.3d", figure=fig, background='w')
brain = Brain("Kamitani_sbj3", "both", "full.flat.patch.3d", figure=fig, cortex='bone')
# brain = Brain("Kamitani_sbj3", "lh", "inflated", figure=fig, cortex='bone')

# brain.add_label(label='V1_exvivo',hemi='lh')
# brain.add_label(label='V1_exvivo',hemi='rh')
#
# overlay_file = "../examples/example_data/lh.sig.nii.gz"
# brain.add_overlay(overlay_file,hemi='lh')
overlay_filename = "fsl_10k_corr_Kamitani_sbj3_lh_flat.nii"
overlay_path = os.path.join(cortical_maps_path, overlay_filename)
# brain.add_overlay(overlay_path, hemi='lh', min=0.001, max='actual_max', sign='pos')
scalar_data = np.nan_to_num(np.ravel(nib.load(overlay_path).get_data(), order='F'))
brain.add_data(scalar_data, hemi='lh', thresh=1e-5, colormap="RdPu")

# cam = fig.scene.camera
# cam.zoom(1.85)

mlab.savefig(cortical_maps_path + '/test.png',figure=fig,magnification=5) # save a high-res figure