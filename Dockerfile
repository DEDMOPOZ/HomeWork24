FROM python:3.9

RUN uname -a
RUN apt update && apt install -y python-setuptools

WORKDIR /srv/project

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ src/

WORKDIR /srv/project/src

RUN useradd -ms /bin/bash admin
RUN chown -R admin:admin /srv/project
RUN chmod 755 /srv/project
USER admin

RUN mkdir /srv/project/static
