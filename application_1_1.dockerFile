FROM python:3.8-slim-buster


COPY . /backend
COPY google/sapient-climate-350213-3fb7c260e157.json /backend
ENV GOOGLE_APPLICATION_CREDENTIALS "/backend/google/sapient-climate-350213-3fb7c260e157.json"
WORKDIR /backend/src
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/src"
WORKDIR /backend
CMD ["python", "src/main_1_1.py"]
#CMD ["ls"]

