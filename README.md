# Interrogat'IF
Automatic quiz generation for teachers and students.<br/>
As part of the SMART project in 4th year in computer science at INSA Lyon.

[Watch the trailer](https://drive.google.com/file/d/1cJHEJfIYYeMgE446lCG5DqxisWigEIg7/view?usp=sharing)

## Install a virtual environment

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

# Install all dependencies
python3 -m pip install -r requirements.txt

# Finally, download glove's word embeddings at:
# https://www.kaggle.com/danielwillgeorge/glove6b100dtxt
# and place it here: ./data/embeddings/word2vec-glove.6B.100d.txt
# (this file was too big for GitHub)

# Leave the virtual environment
deactivate
```

## Generate questions

Start Interrogat'IF with `python3 interrogatif.py`.
