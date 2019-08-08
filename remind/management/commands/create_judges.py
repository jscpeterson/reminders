from django.core.management.base import BaseCommand, CommandError
from cases.models import Judge


class ListLengthException(Exception):
    pass


class JudgeExistsException(Exception):
    pass


class Command(BaseCommand):
    help = 'Creates judges in database'

    def _read_source(self, file_path):
        """ Returns a list of lines from a file path"""
        with open(file_path) as source:
            return [line.replace('\n', '') for line in source]

    def _create_judge(self, judge):
        """
        Creates a judge object based on a given list of first_name, last_name or first_name, middle_name, last_name
        """

        names = judge.split(' ')

        if len(names) == 2:
            if Judge.objects.filter(first_name=names[0], last_name=names[1]).exists():
                raise JudgeExistsException()
            Judge.objects.create(
                first_name=names[0],
                last_name=names[1],
            )
        elif len(names) == 3:
            if Judge.objects.filter(first_name=names[0], middle_name=names[1], last_name=names[2]).exists():
                raise JudgeExistsException()
            Judge.objects.create(
                first_name=names[0],
                middle_name=names[1],
                last_name=names[2],
            )
        else:
            raise ListLengthException('Expected a list of length 2 or 3, got "{judge}" with {length} words. '
                                      'Check source file.'.format(judge=judge, length=len(names)))

    def add_arguments(self, parser):
        """ Adding argument for file name """
        parser.add_argument('--source', type=str, required=True)

    def handle(self, *args, **kwargs):
        """ Handles creating judges """

        judges = self._read_source(kwargs['source'])
        successes = 0
        failures = 0
        skips = 0

        for index, judge in enumerate(judges):
            try:
                self._create_judge(judge)
                successes += 1
            except JudgeExistsException:
                skips += 1
            except Exception as e:
                print('Failure on line {line}: {exception}'.format(line=index, exception=e))
                failures += 1

        print('Created {successes} judges with {failures} failures.\n'
              'Skipped {skips} judges already present in the database.\n'
              '{total} judges exist in the database.'.format(
                successes=successes,
                failures=failures,
                skips=skips,
                total=len(Judge.objects.all())
                ))
