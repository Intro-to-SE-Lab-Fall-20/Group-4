#! /bin/sh

PYTHON_BINARY=${PYTHON:-python3}

# Setup Python environment
if [[ ! -d "env" ]]; then
    $PYTHON_BINARY -m venv env
fi

source env/bin/activate
pip --disable-pip-version-check install -q -r requirements.txt

# Launch the server; 'python' now points to $PYTHON_BINARY in the env
python polymail/manage.py runserver
