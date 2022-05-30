## Admin installed packages

sudo apt update && apt install -y csh tcsh libxt-dev libncurses-dev xaw3dg xaw3dg-dev libxaw7-dev wget vim make binutils gcc gfortran

## User package building

mkdir $HOME/gipsy
cd $HOME/gipsy/
wget https://ftp.astro.rug.nl:9090/gipsy/gipsy64/src/gipsy64python3_src.tar.gz
gunzip < gipsy64python3_src.tar.gz | tar xvf -
export gip_root=`\pwd`

Incase ./mkbookkeeper.csh fails with missing variables just add them manually.
export gip_sub=$gip_root/sub
export gip_tsk=$gip_root/tsk
export gip_dat=$gip_root/dat
export gip_doc=$gip_root/doc
export gip_exe=$gip_root/exe
export gip_loc=$gip_root/loc

export SHELL=/bin/csh

cd sys
csh mkclient.csh 103
mv clients.new ../loc/clients
exec /bin/csh --login
source cshrc.csh 
cp setup.mgr ../loc/setup
./install.csh
./mkbookkeeper.csh
mv bookkeeper.new bookkeeper

vi ~/.cshrc
setenv gip_root $HOME/gipsy
source $gip_root/sys/gipenv.csh

p -update > & p.log &

gipsy
