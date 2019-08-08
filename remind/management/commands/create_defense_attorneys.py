import csv

from django.core.management.base import BaseCommand, CommandError
from remind.models import DefenseAttorney


class ListLengthException(Exception):
    pass


class ObjectExistsException(Exception):
    pass


class Command(BaseCommand):
    help = 'Creates defense attorneys in database, based on a csv with their name and firm. By no means ' \
           'comprehensive but will give some initial data'

    def _read_source(self, file_path):
        """ Returns a list of lines from a file path"""
        with open(file_path) as source:
            csv_reader = csv.DictReader(source, delimiter=',')
            return [row for row in csv_reader]

    def _create_defense_attorney(self, row):
        """
        Creates a defense attorney based on a csv record
        """

        firm = row['firm'] if row['firm'] is not '' else None
        names = row['attorney'].split(' ')

        if len(names) == 2:
            if DefenseAttorney.objects.filter(
                first_name=names[0],
                last_name=names[1],
                firm=firm,
            ).exists():
                raise ObjectExistsException()
            DefenseAttorney.objects.create(
                first_name=names[0],
                last_name=names[1],
                firm=firm
            )
        elif len(names) == 3:
            if DefenseAttorney.objects.filter(
                first_name=names[0],
                middle_name=names[1],
                last_name=names[2],
                firm=firm,
            ).exists():
                raise ObjectExistsException()
            DefenseAttorney.objects.create(
                first_name=names[0],
                middle_name=names[1],
                last_name=names[2],
                firm=firm,
            )
        else:
            raise ListLengthException('Expected a list of length 2 or 3, got "{names}" with {length} words. '
                                      'Check source file.'.format(
                                        names=names,
                                        length=len(names)
                                        ))

    def add_arguments(self, parser):
        """ Adding argument for file name """
        parser.add_argument('--source', type=str, required=True)

    def handle(self, *args, **kwargs):
        """ Handles creating attorneys """

        data = self._read_source(kwargs['source'])
        successes = 0
        failures = 0
        skips = 0

        for index, row in enumerate(start=1, iterable=data):
            try:
                self._create_defense_attorney(row)
                successes += 1
            except ObjectExistsException:
                skips += 1
            except Exception as e:
                print('Failure on line {line}: {exception}'.format(line=index, exception=e))
                failures += 1

        print('Created {successes} attorneys with {failures} failures.\n'
              'Skipped {skips} attorneys already present in the database.\n'
              '{total} defense attorneys exist in the database.'.format(
                successes=successes,
                failures=failures,
                skips=skips,
                total=len(DefenseAttorney.objects.all())
                ))
