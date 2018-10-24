#!/bin/env python
#==========================
# author: Maria Elidaiana
# email: mariaeli@brandeis.edu
#==========================

'''
This code get the (RA,DEC) in the Blink images and convert from sexagesimal to degrees. 
'''
import astropy
import astropy.coordinates as coord
import astropy.units as u
import fitsio
import glob
import numpy as np

fitsdir = glob.glob("/share/storage1/blink/*.fz")

ext=0
ras, decs=[],[]
ras_ori, decs_ori = [],[]
for i in range(len(fitsdir)):
    image,hdr=fitsio.read(fitsdir[i], ext=ext, header=True)
    try:
        ra_sexag = coord.Angle(hdr["RA"], unit=u.hour)
        ra_deg = float(ra_sexag.to_string(unit='degree', decimal=True))

        dec_sexag = coord.Angle(hdr["DEC"], unit=u.degree)
        dec_deg = float(dec_sexag.to_string(unit='degree', decimal=True))
        
        
        ras.append(ra_deg)
        decs.append(dec_deg)
        ras_ori.append(hdr["RA"])
        decs_ori.append(hdr["DEC"])
        
        
    except (KeyError,astropy.coordinates.errors.IllegalHourError):
        pass
    print 'Finished: ', fitsdir[i]

ras=np.array(ras)
decs=np.array(decs)
ras_ori=np.array(ras_ori)
decs_ori=np.array(decs_ori)

np.savetxt("blink_coords.txt", np.c_[ras,decs])
np.savetxt("blink_coords_sexag.txt", np.c_[ras_ori,decs_ori], fmt='%.32s',)
