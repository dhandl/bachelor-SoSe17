
source /cvmfs/sft.cern.ch/lcg/views/LCG_latest/x86_64-slc6-gcc49-opt/setup.sh

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

export WorkDir=`pwd`

export RGS_PATH=`pwd`/ML/examples/public/RGS
export PYTHONPATH=$RGS_PATH/python:$PYTHONPATH
export LD_LIBRARY_PATH=$RGS_PATH/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$RGS_PATH/lib:$DYLD_LIBRARY_PATH

export FBM_PATH=`pwd`/ML/fbm.2004-11-10
export PATH=$FBM_PATH/net:$PATH
export PATH=$FBM_PATH/dist:$PATH
export PATH=$FBM_PATH/mc:$PATH
export PATH=$FBM_PATH/util:$PATH

export PATH=$PATH:$WorkDir/ML/scripts
export PATH=$PATH:$WorkDir/ML/bin
export PYTHONPATH=$PYTHONPATH:$WorkDir/python

lsetup "root 6.08.06-x86_64-slc6-gcc49-opt"

