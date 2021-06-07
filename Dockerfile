FROM python:3.9

RUN uname -a
RUN apt update && apt install -y python-setuptools

WORKDIR /srv/project
COPY requirements.txt /tmp/requirements.txt
COPY src/ src/

RUN pip install -r /tmp/requirements.txt
