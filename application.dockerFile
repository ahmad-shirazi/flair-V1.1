FROM python:3.8-slim-buster


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

#RUN apt-get install -y build-essentials
RUN apt-get install -y wget
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
#CMD ["ls"]
ENV CONDA_DIR /opt/conda

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda install -c conda-forge poppler

COPY . /backend
COPY google/sapient-climate-350213-3fb7c260e157.json /backend
ENV GOOGLE_APPLICATION_CREDENTIALS "/backend/google/sapient-climate-350213-3fb7c260e157.json"
WORKDIR /backend/src
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/src"
WORKDIR /backend
CMD ["python", "src/main.py"]
#CMD ["ls"]

