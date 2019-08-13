from random import randint
from django.core.management.base import BaseCommand
from cases.models import Case
from remind.models import Deadline


class Command(BaseCommand):
    help = 'Clones a case from the case number passed in as an argument for stress testing purposes where the specific ' \
           'data does not matter. --clones is the number of clones that will be created'

    def add_arguments(self, parser):
        parser.add_argument('--case', type=str, required=True)
        parser.add_argument('--clones', type=int, required=True)

    def handle(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs['case'])
        poor_bastard = case.prosecutor
        print('Creating cases with deadlines for {poor_bastard}...'.format(poor_bastard=poor_bastard))
        for i in range(kwargs['clones']):

            new_case = Case.objects.get(pk=case.pk)

            # Creates a random new case number
            new_case.case_number = '2019-{random1}-{random2}'.format(
                random1=randint(10000, 99999),
                random2=randint(10000, 99999),
            )
            new_case.cr_number = '2019-{random1}-{random2}'.format(
                random2=randint(10000, 99999),
                random1=randint(10000, 99999),
            )

            # Clones case by resetting its pk
            new_case.pk = None
            new_case.save()

            # Clones deadlines onto new case
            for deadline in Deadline.objects.filter(case=case):
                new_deadline = Deadline.objects.get(pk=deadline.pk)
                new_deadline.case = new_case
                new_deadline.pk = None
                new_deadline.save()

            print('{i}: Created new case'.format(i=i))

        print('{poor_bastard} now has {cases} cases in the database with a total of {deadlines} deadlines.'.format(
            poor_bastard=poor_bastard,
            cases=len(Case.objects.filter(prosecutor=poor_bastard)),
            deadlines=len(Deadline.objects.filter(case__prosecutor=poor_bastard)),
        ))
