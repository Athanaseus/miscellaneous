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
