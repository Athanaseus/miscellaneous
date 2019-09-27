import xarrayms as xm                                                                                                                                                                                                                                                                                                         
import matplotlib.pyplot as plt
from dask import compute
import numpy as np
from time import time


ms_name ="path/to/ms/file"

#group according to SPW
ms = xm.xds_from_ms(ms_name, group_cols=['DATA_DESC_ID'], ack=False)[0]

#get the u and v coordinates from xarray
u = ms.UVW.sel(uvw=0).data
v = ms.UVW.sel(uvw=1).data

#use this function to get the actual values from dask
#because dask evalutes lazily
u, v = compute(u, v)

# Frequecies (64 channels)
c = 299792458  # meters per second
freqs = range(1420000000, 1548000000, 2000000)

u_lambda, v_lambda = [], []

start_time = time()
for i, _u in enumerate(u):
    print("Progress: {:f} %".format((float(i)/len(u))*100.0))
    if i%50 == 0:
        for freq in freqs:
            u_lambda.append(u[i]*freq/c)
            v_lambda.append(v[i]*freq/c)

u_klambda, v_klambda  = np.array(u_lambda)/1000.0, np.array(v_lambda)/1000.0
print("Time elapsed for computing lambdas: {:f} seconds".format((time() - start_time)))

#plot both components
#plt.plot(u, v, 'bo', -u, -v, 'ro', markersize=0.8)
start_time = time()
plt.plot(u_klambda, v_klambda, 'r,', -u_klambda, -v_klambda, 'b,', markersize=0.1)
plt.xlabel('u (k$\lambda$)')
plt.ylabel('v (k$\lambda$)')
print("Number of data points: u={:d}".format(2*len(u_lambda)))

print("Time elapsed for ploting lambdas: {:f} seconds".format((time() - start_time)))
plt.savefig('uvcoverage.png')
print("Done!")
