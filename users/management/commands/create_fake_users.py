import os
from django.conf import settings
from django.core.management.base import BaseCommand
from users.models import CustomUser
import configparser
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Creates one user per position in database'
    param_file = os.path.join(settings.BASE_DIR, 'params.ini')

    def handle(self, *args, **kwargs):
        """ Handles creating users """

        positions = dict(((x[1], x[0]) for x in CustomUser.POSITION_CHOICES))
        test_emails = self._get_email_addresses()

        for position_label, position_index in positions.items():
            if position_index == CustomUser.PROSECUTOR:
                first_name = 'Pancho'
                last_name = 'Villa'
            else:
                first_name = faker.first_name()
                last_name = faker.last_name()
            
            CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=first_name[0] + last_name,
                position=position_index,
                email=test_emails.get(position_label),
            )
            print('Created', position_label)

    def _get_email_addresses(self):
        """ Returns dictionary of email addresses to use for each position """
        # Start config parser to read parameters from INI file
        emails = self._load_emails()
        return {label: emails.get(label.lower() + '_email')
                for _, label in CustomUser.POSITION_CHOICES}

    def _load_emails(self):
        """ Loads emails from config file """
        config = configparser.ConfigParser()

        with open(self.param_file, 'r') as f:
            config.read_file(f)
        return dict(config['TEST'])
