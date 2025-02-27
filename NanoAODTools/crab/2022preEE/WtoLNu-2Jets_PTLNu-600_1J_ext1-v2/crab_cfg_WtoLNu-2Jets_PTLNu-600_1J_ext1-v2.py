from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WtoLNu-2Jets_PTLNu-600_1J_ext1-v2_20250223_203356'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../Run3_keep_and_drop_MC.txt']

config.section_("Data")
config.Data.inputDataset = '/WtoLNu-2Jets_PTLNu-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jelee/crab_NanoAOD/2022preEE/WtoLNu-2Jets_PTLNu-600_1J_ext1-v2'
config.Data.publication = False
config.Data.outputDatasetTag = 'WtoLNu-2Jets_PTLNu-600_1J_ext1-v2'

config.section_("Site")
config.Site.storageSite = "T3_KR_KNU"
