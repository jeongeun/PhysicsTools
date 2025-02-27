from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'TBbartoLplusNuBbar-s-ch'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../Run3_keep_and_drop_MC.txt']

config.section_("Data")
config.Data.inputDataset = '/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jelee/crab_NanoAOD/2022preEE/TBbartoLplusNuBbar-s-ch'
config.Data.publication = False
config.Data.outputDatasetTag = 'TBbartoLplusNuBbar-s-ch'

config.section_("Site")
config.Site.storageSite = "T3_KR_KNU"
