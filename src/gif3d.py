# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 09:53:59 2022

@author: hpeng
"""

import numpy as np
import matplotlib
#	matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import imageio as io
import os

import stata_setup
stata_setup.config("C:/Program Files/Stata17", "mp")
from pystata import stata

stata.run('sysuse sandstone, clear')
D = stata.nparray_from_data("northing easting depth")

ax = plt.axes(projection='3d')
plt.xticks(np.arange(60000, 90001, step=10000))
plt.yticks(np.arange(30000, 50001, step=5000))
ax.plot_trisurf(D[:,0], D[:,1], D[:,2], cmap=plt.cm.Spectral, edgecolor='none')

for i in range(0, 360, 10):
	ax.view_init(elev=10., azim=i)
	plt.savefig("../gif/sandstone"+str(i)+".png")
	
with io.get_writer('../gif/sandstone.gif', mode='I', duration=0.5) as writer:
	for i in range(0, 360, 10):
		image = io.imread("../gif/sandstone"+str(i)+".png")
		writer.append_data(image)
writer.close()
