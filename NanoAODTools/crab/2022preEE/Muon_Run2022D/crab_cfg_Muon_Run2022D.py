from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'Muon_Run2022D_20250223_203346'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py', '../../Run3_keep_and_drop_Data.txt']

config.section_("Data")
config.Data.inputDataset = '/Muon/Run2022D-22Sep2023-v1/NANOAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/jelee/crab_NanoAOD/2022preEE/Muon_Run2022D'
config.Data.publication = False
config.Data.outputDatasetTag = 'Muon_Run2022D'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json'

config.section_("Site")
config.Site.storageSite = "T3_KR_KNU"
