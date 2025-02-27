# Instruction for Skimming NanoAOD (in Run-3) using CRAB3

### Environment set (lxplus8)

```
ssh <user>@lxplus8.cern.ch

export SCRAM_ARCH=el8_amd64_gcc11
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
voms-proxy-init --voms cms -valid 100:00 -rfc
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```
### Checkout instruction (CMSSW 13X)

```
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src
cmsenv

git clone https://github.com/jeongeun/PhysicsTools.git PhysicsTools/NanoAODTools
#git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j4
```

#### Simple recipe (Run on LXPLUS8)

```
cd PhysicsTools/NanoAODTools/crab
python3 genCrabconfig.py InputDataset_2022.txt ./2022preEE
cd 2022preEE/Muon_Run2022C/
crab submit -c crab_cfg_Muon_Run2022C.py

```

### Description for scripts

All scripts are in direcotry `crab`, and all CRAB related jobs are done under this directory.

* Process list `InputDataset_2022.txt` : Process name and its DAS path for each subera written in each file.

* Python script `genCrabconfig.py` : Generates directorie and CRAB scripts for the processes defined in the process list. Run by `python3 genCrabconfig.py <Process list> <output directory>`. For example, `python3 genCrabconfig.py InputDataset_2022.txt 2022preEE` will generate `2022preEE/<process name>` directories, and CRAB scripts under each of them.

* Skimming list `Run3_keep_and_drop.txt` : Branch skimming defined in these files.

* Directories `2022preEE` : Directories of each process, and thier CRAB scripts will be stored under this directories.


### Description for each CRAB script

There are four different scripts produced under `<era>/<process name>` directory
Unlike many other CMSSW modules, the NanoAOD post processor does not use EDProducer/EDAnalyzer etc. This can be ran with python.
To do so, we submit fake PSet to CRAB which does nothing, and use `crab_script.sh` to run the actual post processing script (`crab_script.py`) using python.

* `PSet.py` : Fake PSet for CRAB submission. No need to change this file.

* `crab_scrtip.sh` : The shell script which CRAB job executes. Nothing done in this script, it just runs the `crab_script.py` using python, not cmsRun. No need to change this file.

* `crab_cfg_<process name>.py` : CRAB configuration file. Input process, output file site and directory, GoldenJson for Run/Lumi skimming are defined here.

* `crab_script.py` : This script is where actual post processor is defined. Currently only branch skimming, and Run/Lumi skimming for Data is applied. One can modify the post processor to add cut, or some other features defined in post processor class.




## nanoAOD-tools

A minimal set of python tools to post-process NanoAODs to:
* skim branches
* add variables
* produce plots
* perform analyses.

It can be used directly from a CMSSW environment, or checked out as a standalone package.
The framework part of NanoAODTools is maintained as a CMSSW package, in PhysicsTools/NanoAODTools.
Originally imported to CMSSW from [cms-nanoAOD/nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools) (post-processor functionality only).


#### Listup your input dataset

```
#2022 preEE rereco data, Muon and EGamma
das_client --query="dataset=/*Muon/Run2022*-22Sep2023-v1/NANOAOD" >> samples_22.txt
das_client --query="dataset=/EGamma/Run2022*-22Sep2023-v1/NANOAOD" >> samples_22.txt
#DY bg
das_client --query="dataset=/WtoLNu*4Jets*MLNu*TuneCP5*13p6TeV*madgraphMLM*pythia8/Run3Summer22NanoAODv12*/NANO*SIM" >> samples_22.txt
das_client --query="dataset=/WtoLNu-2Jets_PTLNu-*_*J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/DYto2E_MLL-*/Run3Summer22NanoAODv12*/NANO*SIM" >> samples_22.txt
das_client --query="dataset=/DYto2Mu_MLL-*/Run3Summer22NanoAODv12*/NANO*SIM" >> samples_22.txt
das_client --query="dataset=/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
#Diboson bg
das_client --query="dataset=/WW_TuneCP5_13p6TeV_pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WZ_TuneCP5_13p6TeV_pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/WZtoL3Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
#TTbar bg
das_client --query="dataset=/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TTtoLNu2Q_TuneCP5_13p6TeV-powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
#SingleT bg
das_client --query="dataset=/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
das_client --query="dataset=/TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
#QCD
das_client --query="dataset=/QCD_PT-*_TuneCP5_13p6TeV_pythia8/Run3Summer22NanoAODv12*/NANOAODSIM" >> samples_22.txt
```

#### Created dataset list:

```
ls PhysicsTools/NanoAODTool/crab/InputDataset_2022.txt
```


#### Define your skimming list: keep and drop branch

```
ls PhysicsTools/NanoAODTool/crab/Run3_keep_and_drop.txt #2022 preEE
```

#### To make crab cfg files to skimming your input datasets

```
python3 genCrabconfig.py [Dataset List] [DirectoryName]
```

#### Crab submit (set proper output site in crab_cfg, T3_KR_KNU or KISTI as you want)

```
cd 2022preEE/SingleMuon_Run2022B
crab submit -c crab_cfg_SingleMuon_Run2018B.py
```

#### Automatic crab submit and resubmit (if submitfailed)

```
# Automatic submit 
# Three arguments : 
# base_directory --parallel=1 (default), --dry-run=True/False (default=True, not running just showing the commandline)
#./submit_crab_jobs.sh <CrabWorkingDirectory> [--dry-run=] [--parallel=1]
./submit_crab_jobs.sh 2022preEE --dry-run=False --parallel=4

# Automatic resubmit 
# Three arguments : 
# base_directory --parallel=1 (default) --doresubmit=0/1 (default=0, not resubmit just showing the problematic processes)
./check_crabjob.sh 2022preEE --parallel=4 --doresubmit=0
```

