
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

export WorkDir=`pwd`
export PATH=$PATH:$WorkDir/scripts
export PYTHONPATH=$PYTHONPATH:$WorkDir/python

lsetup "root 6.08.06-x86_64-slc6-gcc49-opt"

