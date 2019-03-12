#!usr/bin/env python

import os.sys
import ROOT
import subprocess
import json
from glob import glob

FILE_PATTERN = "results/Stop1L_Moriond19_bWN_oneBin_140p5fb{type}_{mT}_{mX}_plot_Output_fixSigXSecNominal_hypotest.root"
JSON_PATTERN = 'Stop1L_Moriond19_bWN_oneBin_140p5fb{type}_{mT}_{mX}_plot_Output_fixSigXSecDown_hypotest__1_harvest_list.json'

HARVEST = [
    ### bWN ###
    {'type':'bWN', 'mT':400, 'mX':235, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':400, 'mX':250, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':400, 'mX':280, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':400, 'mX':310, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':450, 'mX':285, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':450, 'mX':300, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':450, 'mX':330, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':450, 'mX':360, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':500, 'mX':335, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':500, 'mX':350, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':500, 'mX':380, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':500, 'mX':410, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':550, 'mX':385, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':550, 'mX':400, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':550, 'mX':430, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':550, 'mX':460, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':600, 'mX':435, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':600, 'mX':450, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':600, 'mX':480, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':600, 'mX':510, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':650, 'mX':485, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':650, 'mX':500, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':650, 'mX':530, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':650, 'mX':560, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':700, 'mX':535, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':700, 'mX':550, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':700, 'mX':580, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':700, 'mX':610, 'yield':0, 'var':0},

    {'type':'bWN', 'mT':750, 'mX':585, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':750, 'mX':600, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':750, 'mX':630, 'yield':0, 'var':0},
    {'type':'bWN', 'mT':750, 'mX':660, 'yield':0, 'var':0},

    ### bffN ###
    {'type':'bffN', 'mT':300, 'mX':220, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':300, 'mX':250, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':300, 'mX':280, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':300, 'mX':293, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':350, 'mX':270, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':350, 'mX':300, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':350, 'mX':330, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':350, 'mX':343, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':400, 'mX':320, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':400, 'mX':350, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':400, 'mX':380, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':400, 'mX':393, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':450, 'mX':370, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':450, 'mX':400, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':450, 'mX':430, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':450, 'mX':443, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':500, 'mX':420, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':500, 'mX':450, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':500, 'mX':480, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':500, 'mX':493, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':550, 'mX':470, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':550, 'mX':500, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':550, 'mX':530, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':550, 'mX':543, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':600, 'mX':520, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':600, 'mX':550, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':600, 'mX':580, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':600, 'mX':593, 'yield':0, 'var':0},

    {'type':'bffN', 'mT':650, 'mX':570, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':650, 'mX':600, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':650, 'mX':630, 'yield':0, 'var':0},
    {'type':'bffN', 'mT':650, 'mX':643, 'yield':0, 'var':0},

    ### tN ###
    {'type':'tN', 'mT':190, 'mX':17,  'yield':0, 'var':0},
    {'type':'tN', 'mT':400, 'mX':200, 'yield':0, 'var':0},
    {'type':'tN', 'mT':500, 'mX':300, 'yield':0, 'var':0},
    {'type':'tN', 'mT':500, 'mX':312, 'yield':0, 'var':0},
    {'type':'tN', 'mT':500, 'mX':327, 'yield':0, 'var':0},
    {'type':'tN', 'mT':550, 'mX':350, 'yield':0, 'var':0},
    {'type':'tN', 'mT':550, 'mX':362, 'yield':0, 'var':0},
    {'type':'tN', 'mT':550, 'mX':377, 'yield':0, 'var':0},
    {'type':'tN', 'mT':600, 'mX':400, 'yield':0, 'var':0},
    {'type':'tN', 'mT':600, 'mX':412, 'yield':0, 'var':0},
    {'type':'tN', 'mT':600, 'mX':427, 'yield':0, 'var':0},
    {'type':'tN', 'mT':650, 'mX':450, 'yield':0, 'var':0},
    {'type':'tN', 'mT':650, 'mX':462, 'yield':0, 'var':0},
    {'type':'tN', 'mT':650, 'mX':477, 'yield':0, 'var':0},
    {'type':'tN', 'mT':700, 'mX':500, 'yield':0, 'var':0},
]

def main():

  for smp in HARVEST:
    iF = glob(FILE_PATTERN.format(smp['type'], smp['mT'], smp['mX']))
    jF = glob(JSON_PATTERN.format(smp['type'], smp['mT'], smp['mX']))
    subprocess.call('GenerateJSONOutput.py -i {} -f "hypo_{}_%f_%f" -p "mT:mX"'.format(iF, smp['type']), shell=True)
    with open(jF,'r') ad f:
      sig = json.load(f) 
    smp['CLsexp'] = sig[0]['CLsexp']
    smp['CLs'] = sig[0]['CLs']
    smp['clsd1s'] = sig[0]['clsd1s']
    smp['clsu1s'] = sig[0]['clsu1s']
    
  print HARVEST

if __name__ == "__main__":
  main()
