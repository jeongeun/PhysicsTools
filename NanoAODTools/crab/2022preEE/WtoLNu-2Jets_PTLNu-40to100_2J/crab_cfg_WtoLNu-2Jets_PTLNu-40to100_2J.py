from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WtoLNu-2Jets_PTLNu-40to100_2J_20250223_203339'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../Run3_keep_and_drop_MC.txt']

config.section_("Data")
config.Data.inputDataset = '/WtoLNu-2Jets_PTLNu-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jelee/crab_NanoAOD/2022preEE/WtoLNu-2Jets_PTLNu-40to100_2J'
config.Data.publication = False
config.Data.outputDatasetTag = 'WtoLNu-2Jets_PTLNu-40to100_2J'

config.section_("Site")
config.Site.storageSite = "T3_KR_KNU"
