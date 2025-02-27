#!/bin/bash

# Usage: ./submit_crab_jobs.sh <CrabWorkingDirectory> [--dry-run] [--parallel=N]

if [ -z "$1" ]; then
    echo "Error: No argument provided. Please specify the Crab working directory."
    echo "Usage: $0 <CrabWorkingDirectory> [--dry-run] [--parallel=N]"
    exit 1
fi

CrabWorkingDirectory="$1"
DryRun=false
ParallelJobs=1

for arg in "$@"; do
    case $arg in
        --dry-run)
            DryRun=true
            shift
            ;;
        --parallel=*)
            ParallelJobs="${arg#*=}"
            shift
            ;;
    esac
done

# Check availability of CRAB command
if ! command -v crab &> /dev/null; then
    echo "Error: CRAB command not found. Please ensure CRAB is installed and available in your PATH."
    exit 1
fi

# Check working directory for Crab
if [ ! -d "$CrabWorkingDirectory" ]; then
    echo "Error: Directory '$CrabWorkingDirectory' not found!"
    exit 1
fi

#  move to working directory
cd "$CrabWorkingDirectory" || { echo "Error: Cannot access $CrabWorkingDirectory"; exit 1; }

SAMPLES=$(find . -maxdepth 1 -type d -not -path '.' | sed 's|^\./||')

submit_crab_job() {
    SAMPLE="$1"
    echo "@@@ Starting Crab Submit for ${SAMPLE} process"
    cd "$SAMPLE" || { echo "Error: Cannot access $SAMPLE"; exit 1; }
    if [ -f "crab_cfg_${SAMPLE}.py" ]; then
        if [ "$DryRun" = true ]; then
            echo "[Dry Run] crab submit -c crab_cfg_${SAMPLE}.py"
        else
            echo "Submitting job for ${SAMPLE}..."
            crab submit -c "crab_cfg_${SAMPLE}.py"
        fi
    else
        echo "!! Not found: crab_cfg_${SAMPLE}.py. Please check!"
    fi
}

export -f submit_crab_job
export DryRun

if [ "$ParallelJobs" -gt 1 ]; then
    echo "Running in parallel mode with $ParallelJobs jobs..."
    echo "$SAMPLES" | xargs -I {} -P "$ParallelJobs" bash -c 'submit_crab_job "$@"' _ {}
else
    for SAMPLE in $SAMPLES; do
	cd "$CrabWorkingDirectory"
        submit_crab_job "$SAMPLE"
    done
fi

echo "All CRAB jobs processed!"
