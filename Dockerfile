FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./requirements/dev.txt /code/requirements/dev.txt
RUN pip install -r /code/requirements/prod.txt

COPY . /code/
WORKDIR /code/

EXPOSE 8000
