import os
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import matplotlib
from mayavi import mlab
from tvtk.api import tvtk
from tvtk.common import configure_input_data
from surfer import Brain
import nibabel as nib
os.environ['SUBJECTS_DIR'] = '/Users/admin/Dropbox (Weizmann Institute)/tunnel/freesurfer_subjects'
cortical_maps_path = '/Users/admin/Dropbox (Weizmann Institute)/tunnel/cortical_maps'

print(__doc__)

# 1) define helper functions


def nannorm(x):
    '''Normalise array betweeen 0-1'''
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


# 2) init brain and get spatial co-ordinates

# params
subjects_dir = os.environ['SUBJECTS_DIR']
hemi = 'lh'
# hemi = 'rh'
# surf = 'white'
surf = 'inflated'

# init figure
fig = mlab.figure()
# b = Brain('fsaverage', hemi, surf, subjects_dir=subjects_dir,
#           background='white', figure=fig)
b = Brain("Kamitani_sbj3", hemi, surf, figure=fig, cortex='bone')

overlay_filename = "fsl_10k_polar_Kamitani_sbj3_{}_flat.nii".format(hemi)
overlay_path = os.path.join(cortical_maps_path, overlay_filename)
scalar_data = np.ravel(nib.load(overlay_path).get_data(), order='F')

overlay_filename = "fsl_10k_snr_Kamitani_sbj3_{}_flat.nii".format(hemi)
overlay_path = os.path.join(cortical_maps_path, overlay_filename)
snr_data = np.ravel(nib.load(overlay_path).get_data(), order='F')

# co-ordinates
x, y, z = b.geo[hemi].coords.T
tris = b.geo[hemi].faces


# 3) generate an rgba matrix, of shape n_vertices x 4

# define color map
# cmap = plt.cm.viridis
cmap = plt.cm.rainbow
# cmap = plt.cm.jet
# cmap = matplotlib.colors.ListedColormap([(1, 0, 0), (0, 0, 1), (0, 1, 0)])

# change colour based on position on the x axis
# hue = norm(x)
# hue = np.nan_to_num(nannorm(scalar_data))
# hue = nan_to_num(interp(scalar_data, (nanmin(scalar_data), nanmax(scalar_data)), (0, 1)))
hue = nan_to_num(interp(((hemi == 'lh')*2 - 1) * scalar_data, (0, 180), (0, 1)))
alpha = (~np.isnan(scalar_data)).astype('float32')
colors = cmap(hue)[:, :3]

# change alpha based on position on the z axis
# alpha = norm(z)

alpha *= interp(snr_data, (nanmin(snr_data), np.nanpercentile(snr_data, 90)), (0.2, 1))
# alpha = np.nan_to_num(nannorm(snr_data.clip(max=np.nanpercentile(snr_data, 90))))
# alpha = np.ones(snr_data.shape)

# combine hue and alpha into a Nx4 matrix
rgba_vals = np.concatenate((colors, alpha[:, None]), axis=1)


# 4) add data to plot

# plot points in x,y,z
mesh = mlab.pipeline.triangular_mesh_source(
    x, y, z, tris, figure=fig)
mesh.data.point_data.scalars.number_of_components = 4  # r, g, b, a
mesh.data.point_data.scalars = (rgba_vals * 255).astype('ubyte')

# tvtk for vis
mapper = tvtk.PolyDataMapper()
configure_input_data(mapper, mesh.data)
actor = tvtk.Actor()
actor.mapper = mapper
fig.scene.add_actor(actor)

# 5) project rgba matrix to flat cortex patch:
fig = mlab.figure()
# b2 = Brain('fsaverage', hemi, 'cortex.patch.flat', subjects_dir=subjects_dir,
#           background='white', figure=fig)
b2 = Brain('Kamitani_sbj3', hemi, 'full.flat.patch.3d',
           # background='white',
           background='black',
           # cortex='bone',
           cortex='classic',
           # cortex˛='low_contrast',
           figure=fig)

print('original rgba_vals.shape:',rgba_vals.shape)
rgba_vals=b2.geo[hemi].surf_to_patch_array(rgba_vals)
print('patch-compatible rgba_vals.shape:',rgba_vals.shape)

# these are the patch's vertices coordinates
x, y, z = b2.geo[hemi].coords.T
tris = b2.geo[hemi].faces

# plot points in x,y,z
mesh = mlab.pipeline.triangular_mesh_source(
    x, y, z, tris, figure=fig)
mesh.data.point_data.scalars.number_of_components = 4  # r, g, b, a
mesh.data.point_data.scalars = (rgba_vals * 255).astype('ubyte')

# tvtk for vis
mapper = tvtk.PolyDataMapper()
configure_input_data(mapper, mesh.data)
actor = tvtk.Actor()
actor.mapper = mapper
fig.scene.add_actor(actor)
mlab.colorbar(cmap)

mlab.savefig(cortical_maps_path + '/test2_{}c.png'.format(hemi),figure=fig,magnification=5) # save a high-res figure