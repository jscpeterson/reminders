from django.core.management.base import BaseCommand
from remind.constants import DEADLINE_DESCRIPTIONS
from remind.models import Case


class Command(BaseCommand):
    help = 'Shows all deadlines with their primary keys on a case from a case number passed in as an argument.'

    def add_arguments(self, parser):
        parser.add_argument('--case', type=str, required=True)

    def handle(self, *args, **kwargs):
        case = Case.objects.get(case_number=kwargs['case'])
        print('Deadlines on Case {cr} involving {defendant}:'.format(
            cr=case.case_number,
            defendant=case.defendant,
        ))
        for deadline in case.deadline_set.all():
            print('PK {pk}: {deadline_desc}'.format(
                pk=deadline.pk,
                deadline_desc=DEADLINE_DESCRIPTIONS[str(deadline.type)].capitalize(),
            ))
