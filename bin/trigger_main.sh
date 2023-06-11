## Setup Different Paths
set -e # To handle exit code ($?)

OWNPATH=`cd $(dirname $0);pwd;cd - >/dev/null 2>/dev/null`
ROOT_DIR=$(dirname $OWNPATH)
SRCPATH=$ROOT_DIR/src
LOGPATH=$ROOT_DIR/logs
jobpid_path=$ROOT_DIR/pids
jobrunner=`basename $0`
jobpidfile=$jobpid_path/$jobrunner.pid

## Print the Usage
usage="This Program will read the $ROOT_DIR/conf/properties.json and credentials.json, get the required details, use these details to setup Project/Job Tempalte/Credentials in AAP.

Usage:
sh $ROOT_DIR/bin/$(basename "$0") create|delete [-h]

where:
    -h  show this help text

Example:
	sh $ROOT_DIR/bin/$(basename "$0") create
"


seed=42

## Display --help
while getopts ':h' option; do
  case "$option" in
    h) echo -e "\n$usage"
       exit
       ;;
  esac
done
shift $((OPTIND - 1))


####################################################
#                 M A I N - P A R T                #
####################################################

echo -e " \n PROJECT: \t Ansible Project Setup \n AUTHOR: \t Naresh Naresh \n CREATED: \t 15th May, 2023 \n PURPOSE: \t To Setup AAP Project, Creds, Job Template etc\n"


## Trigger the Main Python Code
pythonscript=`echo $jobrunner | awk -F'trigger_' '{print $2}' | awk -F'.sh' '{print $1}'`.py
#echo $pythonscript # its value is trigger_WHATEVER_YOU_HAVE.sh

cd $SRCPATH
#(python3.9 $pythonscript > /dev/null 2>&1 &) # if using scr/lib/Logger for logging

python3.9 $pythonscript $1

job_status="$?"

if [ "$job_status" == "0" ]
then
    echo -e "\nJob Completed Successfully\n"
else
    cd $ROOT_DIR
    echo -e "\nJob Failed !!\n"
fi

#END

