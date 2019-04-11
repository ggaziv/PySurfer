import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pylab as pl
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('mycmap', ['green', 'blue', 'red', ])

def make_polar_legend(cmap=cmap):
    #Generate a figure with a polar projection
    # fg = plt.figure(figsize=(8,4))
    fg = plt.figure(figsize=(4,4))
    # ax = fg.add_axes([0.1,0.1,0.9,0.9], projection='polar')
    ax = fg.add_axes([0.,0.,1.,1.], projection='polar')
    ax.set_thetamax(180)
    #define colormap normalization for 0 to 2*pi
    norm = mpl.colors.Normalize(0, np.pi)

    #Plot a color mesh on the polar plot
    #with the color set by the angle

    n = 200  #the number of secants for the mesh
    t = np.linspace(0,np.pi,n)   #theta values
    r = np.linspace(0,1,2)        #raidus values change 0.6 to 0 for full circle
    rg, tg = np.meshgrid(r,t)      #create a r,theta meshgrid
    c = tg                         #define color values as theta value
    im = ax.pcolormesh(t, r, c.T,norm=norm, cmap=cmap)  #plot the colormesh on axis with colormap
    ax.set_yticklabels([])                   #turn of radial tick labels (yticks)
    ax.set_xticklabels([])
    ax.tick_params(pad=15,labelsize=24)      #cosmetic changes to tick labels
    ax.spines['polar'].set_visible(False)    #turn off the axis spine.
    return fg

def make_eccent_legend(cmap=cmap):
    #Generate a figure with a polar projection
    fg = plt.figure(figsize=(4,4))
    # fg = plt.figure()
    ax = fg.add_axes([0.,0.,1.,1.], projection='polar')
    #define colormap normalization for 0 to 2*pi

    #Plot a color mesh on the polar plot
    #with the color set by the angle

    n = 200  #the number of secants for the mesh
    t = np.linspace(0,2*np.pi,n)   #theta values
    r = np.linspace(0,1,n)        #raidus values change 0.6 to 0 for full circle
    norm = mpl.colors.Normalize(0, 2 * np.pi)
    rg, tg = np.meshgrid(r,t)      #create a r,theta meshgrid
    c = rg                         #define color values as theta value
    im = ax.pcolormesh(t, r, c.T[::-1],cmap=cmap)  #plot the colormesh on axis with colormap
    ax.set_yticklabels([])                   #turn of radial tick labels (yticks)
    ax.set_xticklabels([])
    ax.tick_params(pad=15,labelsize=24)      #cosmetic changes to tick labels
    ax.spines['polar'].set_visible(False)    #turn off the axis spine.
    return fg

def make_legend(cmap):
    fg = plt.figure(figsize=(1.5,6))
    ax = fg.add_axes([0.1, 0.1, 0.8, 0.9])

    n = 200  # the number of secants for the mesh
    x = np.linspace(0, 0.01, 2)  # theta values
    y = np.linspace(0, 1, n)  # raidus values change 0.6 to 0 for full circle
    xg, yg = np.meshgrid(x, y)  # create a r,theta meshgrid
    c = yg  # define color values as theta value
    im = ax.pcolormesh(x, y, c, cmap=cmap)  # plot the colormesh on axis with colormap
    ax.set_yticklabels([])  # turn of radial tick labels (yticks)
    ax.set_xticklabels([])
    # ax.spines['polar'].set_visible(False)  # turn off the axis spine.

    # a = np.array([[0,1]])
    # pl.figure()
    # img = pl.imshow(a, cmap=cmap)
    # pl.gca().set_visible(False)
    # # cax = pl.axes([0.1, 0.2, 0.8, 0.6,])
    # cax = pl.axes([0.1, 0.2, 0.11, .8,])
    # pl.colorbar(orientation="vertical", cax=cax)

if __name__ == '__main__':
    pass