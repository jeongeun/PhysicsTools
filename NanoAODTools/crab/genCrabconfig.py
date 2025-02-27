import os
import argparse
import logging
import multiprocessing

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LUMI_MASKS = {
    "2016": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    "2017": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
    "2018": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
    "2022": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json",
    "2023": "https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json",
}

def generate_lumi_mask(process_name):
    """Set correct LUMI_MASK for each dataset"""
    return next((f"config.Data.lumiMask = '{LUMI_MASKS[year]}'\n" for year in LUMI_MASKS if year in process_name), "")

def generate_cfg(process_name, process_path, base_output_directory):
    logging.info(f"Generating scripts for: {process_name}")

    crab_cfg_py = f"crab_cfg_{process_name}.py"
    base_output_name = base_output_directory.strip().replace('/', '')

    output_dir = os.path.join(base_output_directory, process_name)
    os.makedirs(output_dir, exist_ok=True)
    lumi_mask = generate_lumi_mask(process_name)

    branchsel = "Run3_keep_and_drop_MC.txt"

    if any(x in process_name for x in ["Muon", "EGamma"]):
        branchsel = "Run3_keep_and_drop_Data.txt"

    CRAB_CFG = f"""from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '{process_name}'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../{branchsel}']

config.section_("Data")
config.Data.inputDataset = '{process_path}'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jelee/crab_NanoAOD/{base_output_name}/{process_name}'
config.Data.publication = False
config.Data.outputDatasetTag = '{process_name}'
{lumi_mask}
config.section_("Site")
config.Site.storageSite = "T3_KR_KNU"
"""

    CRAB_SCRIPT = f"""#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles, runsAndLumis

p = PostProcessor(".",
                  inputFiles(),
                  branchsel="{branchsel}",
                  provenance=True,
                  fwkJobReport=True,
                  jsonInput=runsAndLumis())
p.run()
print("DONE")
"""

    CRAB_SCRIPT_SH = """#this is not mean to be run locally
echo "Checking if TTY..."
if [ "`tty`" != "not a tty" ]; then
  echo "ERROR: Do not run this script interactively!"
else
  echo "ENVIRONMENT CHECK..."
  env
  echo "VOMS INFO..."
  voms-proxy-info -all
  echo "CMSSW BASE, python path, pwd"
  echo $CMSSW_BASE
  echo $PYTHON_PATH
  echo $PWD
  echo "Found Proxy in: $X509_USER_PROXY"
  python3 crab_script.py $1
fi
"""

    PSET = """import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames=cms.untracked.vstring())
process.source.fileNames = ['../../NanoAOD/test/lzma.root'] #edit if you want local test
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName=cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
"""

    scripts_content = {
        crab_cfg_py      : CRAB_CFG,
        "crab_script.py" : CRAB_SCRIPT,
        "crab_script.sh" : CRAB_SCRIPT_SH,
        "PSet.py"        : PSET
    }

    for filename, content in scripts_content.items():
        with open(os.path.join(output_dir, filename), 'w') as script_file:
            script_file.write(content)
        logging.info(f"Generated: {os.path.join(output_dir, filename)}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate CRAB scripts from a list.")
    parser.add_argument("input_file", help="File containing script names and paths")
    parser.add_argument("output_dir", help="Base output directory for scripts")
    parser.add_argument("--jobs", type=int, default=4, help="Number of parallel jobs (default: 4)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    try:
        with open(args.input_file, 'r') as file:
            scripts = [line.strip().split(',', 1) for line in file if ',' in line.strip()]
    except FileNotFoundError:
        logging.error(f"Error: The file '{args.input_file}' was not found.")
        return

    #multiprocessing
    with multiprocessing.Pool(processes=args.jobs) as pool:
        pool.starmap(generate_cfg, [(pname.strip(), ppath.strip(), args.output_dir) for pname, ppath in scripts])

if __name__ == "__main__":
    main()
