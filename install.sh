command -v pip >/dev/null 2>&1 || { echo >&2 "pip is required in order to install the python dependencies"; exit 1; }
pip install email_validator
