source /cvmfs/sft.cern.ch/lcg/views/LCG_latest/x86_64-slc6-gcc49-opt/setup.sh

export TUTORIALS_PATH=`dirname $(readlink -f $0)`
cd $TUTORIALS_PATH/examples
rm -f public
ln -s /afs/desy.de/user/s/school00/public .
cd -

source $TUTORIALS_PATH/examples/public/RGS/setup.sh
export PATH=$TUTORIALS_PATH/bin:$PATH
export FBM_PATH=$TUTORIALS_PATH/fbm.2004-11-10
export PATH=$FBM_PATH/net:$PATH
export PATH=$FBM_PATH/dist:$PATH
export PATH=$FBM_PATH/mc:$PATH
export PATH=$FBM_PATH/util:$PATH

export PYTHONPATH=$TUTORIALS_PATH/python:$PYTHONPATH

