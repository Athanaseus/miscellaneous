#dpkg -x libcasa-casa4_3.2.1-1kern1_amd64.deb /tmp/libcasa-casa
#dpkg -x libcasa-images4_3.2.1-1kern1_amd64.deb /tmp/libcasa-images
#dpkg -x libcasa-mirlib4_3.2.1-1kern1_amd64.deb /tmp/libcasa-mirlib
#dpkg -x libcasa-python4_3.2.1-1kern1_amd64.deb /tmp/libcasa-python
#dpkg -x libcasa-coordinates4_3.2.1-1kern1_amd64.deb /tmp/libcasa-coordinates
#dpkg -x libcasa-lattices4_3.2.1-1kern1_amd64.deb /tmp/libcasa-lattices
#dpkg -x libcasa-ms4_3.2.1-1kern1_amd64.deb /tmp/libcasa-ms
#dpkg -x libcasa-scimath4_3.2.1-1kern1_amd64.deb /tmp/libcasa-scimath
#dpkg -x libcasa-derivedmscal4_3.2.1-1kern1_amd64.deb /tmp/libcasa-derivedmscal
#dpkg -x libcasa-meas4_3.2.1-1kern1_amd64.deb /tmp/libcasa-meas
#dpkg -x libcasa-msfits4_3.2.1-1kern1_amd64.deb /tmp/libcasa-msfits
#dpkg -x libcasa-scimath-f4_3.2.1-1kern1_amd64.deb /tmp/libcasa-scimath-f
#dpkg -x libcasa-fits4_3.2.1-1kern1_amd64.deb /tmp/libcasa-fits
#dpkg -x libcasa-measures4_3.2.1-1kern1_amd64.deb /tmp/libcasa-measures
#dpkg -x libcasa-python3-4_3.2.1-1kern1_amd64.deb /tmp/libcasa-python3
#dpkg -x libcasa-tables4_3.2.1-1kern1_amd64.deb /tmp/libcasa-tables

import subprocess
from glob import glob
VERSION = '3.2.1'
SOVERSION = '4'
libs = glob('/tmp/libcasa*')
file_name =  '/usr/lib/x86_64-linux-gnu/lib*.so*'
for lib in libs:
   package = lib.split('/')[-1]
   print("Package: {}".format(package))
   command1 = 'mkdir -p {0:s}{1:s}/DEBIAN'
   command2 = 'dpkg-gensymbols -v{0:s} -p{1:s}{2:s} -e{3:s} -O{4:s}{5:s}/DEBIAN/symbols'
   command1 = command1.format(package, SOVERSION)
   command2 = command2.format(VERSION, package, SOVERSION, lib+file_name, package, SOVERSION)
   print('Running: {}'.format(command1))
   process1 = subprocess.run(command1.split(), stdout=subprocess.PIPE)
   print('Running: {}'.format(command2))
   process2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
   print("Done!")
