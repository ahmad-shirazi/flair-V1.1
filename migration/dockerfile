FROM python:3.8-slim-buster

WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./migration/migrate.sh /src/migrate.sh
COPY ./src /src
WORKDIR /src


ENTRYPOINT ["/bin/bash", "/src/migrate.sh"]
CMD ["/src/migrate.sh"]
