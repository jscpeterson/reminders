# Reminders App

This project a solution to the problem of meeting deadlines on a case. It lets the user enter information about deadlines on a case and sends reminder emails.

More details about the app can be found here:

* [Reminders Wiki page](https://gitlab.com/da2nd/reminders/wikis/Reminders)
* [Motions Wiki page](https://gitlab.com/da2nd/reminders/wikis/Motions)

## Getting Started

These instructions will get the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.7
* Docker CE

### Installing
To start the project in a development setting, do the following:

* Clone the project.

  `git clone https://gitlab.com/da2nd/reminders.git`

* Create your virtual environment using Python 3.7. 

  `python3 -m venv env` 

* Install dependencies using `pip`. 

  `pip install -r requirements/dev.txt` 

* Make a copy of .env to hold your environment variables.

  `cp .env.example .env`

* Fill out the values for your development environment.

* Set up the database. 

  `python manage.py migrate`

* (Optional) For ease of development, create fake users
  * Make a copy of params.ini to hold the email addresses for your fake users.
  
    `cp params.ini.example params.ini`
  * Enter the email addresses for your fake users in params.ini. The emails should be real accounts you can check.

* Run the server. 

  `python manage.py runserver`

* To enable sending emails, start Celery.

  * In another terminal window, start a redis service in Docker.

    `docker run -d -p 6379:6379 redis`

  * In another terminal window, start celery beat

    `celery -A reminders beat --loglevel=info`

  * In another terminal window, start celery worker

    `celery -A reminders worker --loglevel=info`

## Running the tests

`python manage.py test`

## Deployment

To deploy in a production environment, do the following steps.

* Ensure that you have Docker and Docker Compose installed.
  * [Installation instructions for Docker on Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
  * [Installation instructions for Docker Compose on Ubuntu](https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-18-04/)

* Make a copy of .env to hold your environment variables.

  `cp .env.prod.example .env`

* Fill out the values for your development environment.

* Start Docker Compose to build and run your images from docker-compose.yml

  `sudo docker-compose up`

## Built With

* [Python](https://www.python.org)
* [Django](https://www.djangoproject.com)
* [PostgreSQL](https://www.postgresql.org)
* [React JS](https://reactjs.org)
* [Docker](https://www.docker.com)
* [Redis](https://redis.io)
* [Celery](https://docs.celeryproject.org/en/latest/)

## Authors

* Eric Verner
* Joseph Peterson
* River Ludington
* Paul Crickard

## License

All rights reserved by the Bernalillo County District Attorney's Office.

## Acknowledgments

* The Bernalillo County DA's office staff for their guidance
  * Raul Torrez
  * Adolfo Mendez
  * Rachel Eagle
  * and others
* [README Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [Review of GitLab Markdown](https://docs.gitlab.com/ee/user/markdown.html)
