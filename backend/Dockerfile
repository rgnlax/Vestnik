FROM python:2.7

WORKDIR /usr/src/generator

ADD requirements.txt requirements.txt
RUN apt-get install libxml2-dev libxslt1-dev zlib1g-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD . /usr/src/generator

CMD gunicorn --bind 0.0.0.0:5000 -w 4 Generator.wsgi

EXPOSE 5000