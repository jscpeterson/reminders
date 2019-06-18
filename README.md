# Reminders App

This project a solution to the problem of meeting deadlines on a case. It lets the user enter information about deadlines on a case and sends reminder emails.

More details about the app can be found here:

* [Wiki page about reminders](https://gitlab.com/da2nd/reminders/wikis/Reminders)
* [Wiki page about motions](https://gitlab.com/da2nd/reminders/wikis/Motions)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.7
* Docker CE

### Installing
To start the project in a development setting, do the following:

Clone the project.

`git clone https://gitlab.com/da2nd/reminders.git`

Create your virtual environment using Python 3.7. 

`python3 -m venv env` 

Install dependencies using `pip`. 

`pip install -r requirements/dev.txt` 

Set up the database. 

`python manage.py migrate`

Run the server. 

`python manage.py runserver`

## Running the tests

`python manage.py test`

## Deployment

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

All rights reserved.

## Acknowledgments

* Raul Torrez, Adolfo Mendez, Rachel Eagle, and other staff at the Bernalillo County DA's office for their guidance
* [README Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [Review of GitLab Markdown](https://docs.gitlab.com/ee/user/markdown.html). 
