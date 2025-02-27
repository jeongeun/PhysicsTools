#this is not mean to be run locally
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
