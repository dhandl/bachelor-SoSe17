#------------------------------------------------------------------------------
# Description: This file contains the commands to run the BNN training.
#              Note: the data-spec format assumes that all inputs in the
#                    training file are used and the last column is the
#                    target.
# Created: Thu Apr 27 10:55:30 2017 by mktrain.py
#------------------------------------------------------------------------------
#	1	SO2tota
#	2	alcohol
#	3	sulfate
#	4	SO2free
#------------------------------------------------------------------------------
echo "File: wino"

net-spec	wino.bin 4 5 1 / - 0.05:0.5 0.05:0.5 - x0.05:0.5 - 100

model-spec	wino.bin binary

data-spec	wino.bin 4 1 2 / wino.dat@2:1001 . wino.dat@2:1001 .

net-gen		wino.bin fix 0.5

mc-spec		wino.bin repeat 20 heatbath hybrid 100:10 0.2

net-mc		wino.bin 1

mc-spec wino.bin repeat 20 sample-sigmas heatbath 0.95 hybrid 100:10 0.2

echo "Start chain"
echo "Use"
echo "   net-display -h wino.bin"
echo "periodically to check the progress of the chain"

time net-mc	wino.bin 250

echo ""
echo "Use"
echo "   netwrite.py -n 100 wino.bin"
echo "to create the BNN function wino.cpp using the last 100 points"
