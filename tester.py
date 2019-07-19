from random import randint

from remind.models import Case, Deadline


class CaseCreator:

    def clone_cases(self, case, number):
        """
        Clones a given case <i>number</i> number of times, and clones it's deadline set, for the purposes of stress
        testing that does not care about the specific data.
        """
        poor_bastard = case.prosecutor
        print('Creating cases with deadlines for {poor_bastard}...'.format(poor_bastard=poor_bastard))
        for i in range(number):

            new_case = Case.objects.get(pk=case.pk)

            # Creates a random new case number
            new_case.case_number = '2019-{random1}-{random2}'.format(
                random1=randint(10000, 99999),
                random2=randint(10000, 99999),
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
