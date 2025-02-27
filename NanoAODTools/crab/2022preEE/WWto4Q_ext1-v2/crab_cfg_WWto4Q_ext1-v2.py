from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WWto4Q_ext1-v2_20250223_203537'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../Run3_keep_and_drop_MC.txt']

config.section_("Data")
config.Data.inputDataset = '/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jelee/crab_NanoAOD/2022preEE/WWto4Q_ext1-v2'
config.Data.publication = False
config.Data.outputDatasetTag = 'WWto4Q_ext1-v2'

config.section_("Site")
config.Site.storageSite = "T3_KR_KNU"
