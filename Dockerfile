FROM ubuntu:18.04
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y software-properties-common

# Completed not yet

EXPOSE 8000
CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=backend.settings.deploy &&\
    python manage.py migrate --settings=backend.settings.deploy &&\
    gunicorn backend.wsgi --env DJANGO_SETTINGS_MODULE=backend.settings.deploy --bind 0.0.0.0:8000 --workers=3 --timeout 180"]