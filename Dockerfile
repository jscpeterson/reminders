FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE reminders.settings.prod
ENV DOCKER_CONTAINER 1

COPY . /code/
RUN pip install -r /code/requirements/prod.txt

WORKDIR /code/

EXPOSE 8000
