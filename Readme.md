curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-395.0.0-darwin-x86_64.tar.gz


tar xvzf ./google-cloud-cli-395.0.0-darwin-x86_64.tar.gz


./google-cloud-sdk/bin/gcloud init

sapient-climate-350213

./google-cloud-sdk/bin/gcloud components update

<!-- Setting up a Python development environment: https://cloud.google.com/python/docs/setup --> 

cd flairsoft
python3 -m venv env
source env/bin/activate
pip install google-cloud-storage


pip install virtualenv
virtualenv env
source env/bin/activate
env/bin/pip install google-cloud-vision


./google-cloud-sdk/bin/gcloud config set accessibility/screen_reader true

./google-cloud-sdk/bin/gcloud projects list

./google-cloud-sdk/bin/gcloud services enable \
    vision.googleapis.com \
    --project=sapient-climate-350213

./google-cloud-sdk/bin/gcloud auth application-default login



import base64
import json
import os

from google.cloud import pubsub_v1
from google.cloud import storage
from google.cloud import translate_v2 as translate
from google.cloud import vision

vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()
storage_client = storage.Client()

project_id = os.environ["GCP_PROJECT"]



pip install nox




export GOOGLE_APPLICATION_CREDENTIALS= /Users/ahmadshirazi/Desktop/FlairSoft/sapient-climate-350213-0e3096f201a7.json

export GOOGLE_APPLICATION_CREDENTIALS= /Users/ahmadshirazi/Desktop/FlairSoft/sapient-climate-350213-3fb7c260e157.json




if you add a python lib need to use \
pip3 freeze > requirements.txt


for adding migration in database:
just a time 
alembic init alembic
alembic upgrade head

for creating each table
alembic revision -m "create document table"


PDF to images
Install poppler: conda install -c conda-forge poppler
Install pdf2image: pip install pdf2image

- sudo docker-compose build --no-cache
- sudo docker-compose up -d
- sudo docker image prune
- sudo docker container prune
