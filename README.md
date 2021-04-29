# Interrogat'IF
Automatic quiz generation for teachers and students.<br/>
As part of the SMART project in 4th year in computer science at INSA Lyon.

## Install the virtual environment

You will need [Python3](https://www.python.org/downloads/) on your machine.

```bash
# Install pip3 and virtualenv
sudo apt-get install python3-pip
sudo pip3 install virtualenv

# Create a virtual environment named "env"
virtualenv env

# Enter the virtual environment
source env/bin/activate  # Unix/MacOS
env\Scripts\activate.bat # Windows

# Install dependencies
python -m pip install -r requirements.txt

# If you add or remove dependencies,
# remember to update requirements.txt
pip3 freeze > requirements.txt

# Leave the virtual environment
deactivate
```

## Execution
Generate a questionnaire based on `input.txt` with `python app.py input.txt`.
