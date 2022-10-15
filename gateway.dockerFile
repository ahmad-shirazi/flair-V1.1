FROM python:3.8-slim-buster


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . /backend
COPY google/sapient-climate-350213-3fb7c260e157.json /backend
ENV GOOGLE_APPLICATION_CREDENTIALS "/backend/google/sapient-climate-350213-3fb7c260e157.json"
#WORKDIR /backend
#RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-395.0.0-darwin-x86_64.tar.gz
#RUN tar xvzf ./google-cloud-cli-395.0.0-darwin-x86_64.tar.gz
#RUN ./google-cloud-sdk/bin/gcloud init
WORKDIR /backend/src
RUN pip install --no-cache-dir -r requirements.txt
#RUN export PYTHONPATH="$PYTHONPATH:/src"
#RUN conda install -c conda-forge poppler
ENV PYTHONPATH "${PYTHONPATH}:/src"
WORKDIR /backend
CMD ["python", "src/gateway.py"]
#CMD ["ls"]

