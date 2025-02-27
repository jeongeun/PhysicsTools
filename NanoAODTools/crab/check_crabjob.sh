#!/bin/bash
# Usage: ./check_crabjob.sh <CrabWorkingDirectory> [--parallel=N]

CrabWorkingDirectory=$1

if [ -z "$CrabWorkingDirectory" ]; then
    echo "Usage: $0 <CrabWorkingDirectory> [--parallel=N] [--doresubmit=0 or 1]"
    exit 1
fi

CurrentDirectory=$PWD
CrabWorkingDirectory="$1"
echo "$CurrentDirectory/$CrabWorkingDirectory"

### default setting
ParallelJobs=1 
doResubmit=0 #Turn off if you really want to resubmit, then switch to 1 

for arg in "$@"; do
    case $arg in
        --parallel=*)
            ParallelJobs="${arg#*=}"
            shift
            ;;
        --doresubmit=*)
            doResubmit="${arg#*=}"
            shift
            ;;
    esac
done

if ! command -v crab &> /dev/null; then
    echo "Error: CRAB command not found. Please ensure CRAB is installed and available in your PATH."
    exit 1
fi

cd "$CrabWorkingDirectory" || { echo "Error: Cannot access directory $CrabWorkingDirectory"; exit 1; }

### Find sample with status = SUBMITFAILED

SUBMITFAILED_SAMPLES=$(find . -maxdepth 1 -type d -not -path '.' | sed 's|^\./||' | while read SAMPLE; do
    STATUS_server=$(crab status -d "$SAMPLE/crab_$SAMPLE" | grep "Status on the CRAB server" | awk '{print $NF}')
    TASK_NAME=$(crab status -d "$SAMPLE/crab_$SAMPLE" | grep "Task name:" | awk '{print $NF}')
    
    if [ "$STATUS_server" == "SUBMITFAILED" ]; then
        echo "$SAMPLE $TASK_NAME"
    fi
done)

STATUSFAILED_SAMPLES=$(find . -maxdepth 1 -type d -not -path '.' | sed 's|^\./||' | while read SAMPLE; do
    STATUS_server=$(crab status -d "$SAMPLE/crab_$SAMPLE" | grep "Status on the CRAB server" | awk '{print $NF}')
    STATUS_scheduler=$(crab status -d "$JOB" | grep "Status on the scheduler:" | awk '{print $NF}')
    
    if [ "$STATUS_scheduler" == "FAILED"  && "$STATUS_server" == "SUBMITFAILED" ]; then
        echo "$SAMPLE $TASK_NAME"
    fi
done)

### Run crab remake and submit

resubmit_crab_job() {

    local SAMPLE TASK_NAME

    read -r SAMPLE TASK_NAME <<< "$1"

    echo "@@@ Resubmitting Crab Job for ${SAMPLE} (Task: ${TASK_NAME})"

    if [ -z "$TASK_NAME" ]; then
        echo "Error: TASK_NAME is empty for $SAMPLE. Skipping."
        return
    fi

   #TARGET_DIR="$CurrentDirectory/$CrabWorkingDirectory/$SAMPLE"
   TARGET_DIR="/afs/cern.ch/work/j/jelee/nanoaod/workspace2025/CMSSW_13_3_0/src/PhysicsTools/NanoAODTools/crab/2022preEE/$SAMPLE"
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Error: Directory does not exist: $TARGET_DIR"
        return
    fi

    cd "$TARGET_DIR" || { echo "Error: Cannot access directory $TARGET_DIR"; return; }

    echo "crab remake --task=$TASK_NAME"
    crab remake --task="$TASK_NAME"

    ### Modify requestName (add submit date/time) in crab_cfg.py
    CONFIG_FILE="crab_cfg_${SAMPLE}.py"
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "!! Not found: $CONFIG_FILE. Skipping submission."
        exit 1
    fi

    NEW_REQUEST_NAME="${SAMPLE}_$(date +%Y%m%d_%H%M%S)"
    sed -i "s/^config.General.requestName =.*/config.General.requestName = '$NEW_REQUEST_NAME'/" "$CONFIG_FILE"

    echo "Updated requestName to: $NEW_REQUEST_NAME"

    ### crab (re)submit
    echo "crab submit -c $CONFIG_FILE"
    crab submit -c "$CONFIG_FILE"
}

export -f resubmit_crab_job

### Always print SUBMITFAILED_SAMPLES, but only execute resubmission if doResubmit=1

if [ -n "$SUBMITFAILED_SAMPLES" ]; then
    echo "Found SUBMITFAILED SAMPLES: $(echo "$SUBMITFAILED_SAMPLES" | wc -l) failed samples..."
    echo "$SUBMITFAILED_SAMPLES"
    echo "======================="
    echo "Found STATUSFAILED SAMPLES: $(echo "$STATUSFAILED_SAMPLES" | wc -l) failed samples..."
    echo "$STATUSFAILED_SAMPLES"
    echo "======================="

    if [ "$doResubmit" -eq 1 ]; then
        echo "$SUBMITFAILED_SAMPLES" | xargs -I {} -P "$ParallelJobs" bash -c 'resubmit_crab_job "$@"' _ {}
    else
        echo "Resubmission is disabled (--doresubmit=0). Please reset=1 if you want resubmission."
    fi
else
    echo "No SUBMITFAILED jobs found."
fi

echo "=============================================================="
echo "All jobs have been checked, failed jobs have been re-submitted."
echo "=============================================================="
