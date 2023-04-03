FROM ubuntu:22.04

RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y software-properties-common
RUN apt-get install -y python3.10 python3.10-distutils python3-pip curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.10 get-pip.py \
    && rm get-pip.py

WORKDIR /drf/
COPY . .

ADD requirements.txt .

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000
# CMD ["bash", "-c", "python3 manage.py collectstatic --noinput --settings=backend.settings.deploy &&\
#     python3 manage.py migrate --settings=backend.settings.deploy &&\
#     gunicorn backend.wsgi --env DJANGO_SETTINGS_MODULE=backend.settings.deploy --bind 0.0.0.0:8000 --workers=3 --timeout 180"]

CMD ["bash", "-c", "python3 manage.py migrate", "python3 manage.py runserver"]