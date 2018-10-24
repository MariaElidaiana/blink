#!/bin/env python
#==========================
# author: Maria Elidaiana
# email: mariaeli@brandeis.edu
#==========================

'''
This code get the result from get_coords.py (RA,DEC) to plot the blink tiles.
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ra, dec = np.genfromtxt('blink_coords.txt', unpack=True)

for i in range(len(ra)):
    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((ra[i] - 1.5, dec[i] - 1.5), 3, 3, facecolor="orange"))
plt.xlim(120,240)
plt.title('BlinK observed tiles')
plt.xlabel('RA')
plt.ylabel('DEC')
plt.plot([133.25, 141.25, 141.25, 133.25, 133.25],[2.75, 2.75, 10.74, 10.74, 2.75], 'b-')
plt.plot([141.25, 160.25, 160.25, 141.25, 141.25],[-1.25,-1.25,11.75,11.75,-1.25], 'b-')
plt.plot([160.25, 170.25, 170.25, 160.25, 160.25], [4, 4, 17, 17, 4], 'b-')
plt.ylim(-40,20)
plt.show()
