BASH_SCRIPT_LOCATION=$(dirname "$(realpath $0)")
PYTHON_SCRIPT_LOCATION="$BASH_SCRIPT_LOCATION/update_google_ddns.py"

SCRIPT_OUTPUT=$(eval $PYTHON_SCRIPT_LOCATION)
echo $SCRIPT_OUTPUT | logger -t update_google_ddns