#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles, runsAndLumis

p = PostProcessor(".",
                  inputFiles(),
                  branchsel="Run3_keep_and_drop_MC.txt",
                  provenance=True,
                  fwkJobReport=True,
                  jsonInput=runsAndLumis())
p.run()
print("DONE")
