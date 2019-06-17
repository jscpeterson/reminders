""" Utility functions for tests """
import os
from users.models import CustomUser
import configparser
from django.conf import settings


param_file = os.path.join(settings.BASE_DIR, 'params.ini')


def create_test_users():
    """ Creates and returns dictionary of test users """
    return {position: CustomUser.objects.create(**params) for position, params in get_test_user_data().items()}


def get_test_user_data():
    """ Returns dict for use in user creation function """
    test_emails = get_email_addresses()
    return {
        CustomUser.get_position_display(CustomUser.SECRETARY): {
            'username': 'palegal',
            'first_name': 'Pear',
            'last_name': 'Alegal',
            'position': CustomUser.SECRETARY,
            'email': test_emails.get(CustomUser.get_position_display(CustomUser.SECRETARY)),
        },
        CustomUser.get_position_display(CustomUser.PROSECUTOR): {
            'username': 'pvilla',
            'first_name': 'Pancho',
            'last_name': 'Villa',
            'position': CustomUser.PROSECUTOR,
            'email': test_emails.get(CustomUser.get_position_display(CustomUser.PROSECUTOR)),
        },
        CustomUser.get_position_display(CustomUser.SUPERVISOR): {
            'username': 'jsuper',
            'first_name': 'John',
            'last_name': 'Super',
            'position': CustomUser.SUPERVISOR,
            'email': test_emails.get(CustomUser.get_position_display(CustomUser.SUPERVISOR)),
        },
    }


def get_email_addresses():
    """ Returns dictionary of email addresses to use for each position """
    # Start config parser to read parameters from INI file
    emails = load_emails()
    return {label: emails.get(label.lower() + '_email')
            for _, label in CustomUser.POSITION_CHOICES}


def load_emails():
    """ Loads emails from config file """
    config = configparser.ConfigParser()

    with open(param_file, 'r') as f:
        config.read_file(f)
    return dict(config['TEST'])


