from django.conf import settings
from faker import Faker
from random import choice

from pytz import timezone

from cases.models import Case, Judge, Defendant, DefenseAttorney
from remind.constants import PUBLIC_DEFENDER_FIRM
from users.models import CustomUser

fake = Faker()


class UserFactory:

    @staticmethod
    def create(position=None):

        if position is None:
            pos = CustomUser.SUPERVISOR
        else:
            pos = position

        first_name = fake.first_name()
        last_name = fake.last_name()
        username = fake.first_name()[0] + fake.last_name()

        return CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            position=pos,
            email=username + '@fake.com',
        )


class JudgeFactory:

    @staticmethod
    def create():
        first_name = fake.first_name()
        last_name = fake.last_name()

        return Judge.objects.create(
            first_name=first_name,
            last_name=last_name,
        )


class DefenseAttorneyFactory:

    @staticmethod
    def create():
        first_name = fake.first_name()
        last_name = fake.last_name()
        firm = PUBLIC_DEFENDER_FIRM if choice([True, False]) else None

        return DefenseAttorney.objects.create(
            first_name=first_name,
            last_name=last_name,
            firm=firm
        )


class DefendantFactory:

    @staticmethod
    def create():
        first_name = fake.first_name()
        last_name = fake.last_name()
        ssn = fake.ssn()
        dob = fake.date_between(start_date='-80y', end_date='-18y')

        return Defendant.objects.create(
            first_name=first_name,
            last_name=last_name,
            ssn=ssn,
            birth_date=dob,
        )


class CaseFactory:
    """ Creates a fake Case with random data """

    @staticmethod
    def create():
        """ Creates a fake criminal Case

        Args:
            num_charges (int): number of fake charges to create
        Returns:
            (Case): fake criminal Case
        """
        return Case.objects.create(
            prosecutor=UserFactory.create(CustomUser.PROSECUTOR),
            secretary=UserFactory.create(CustomUser.SECRETARY),
            supervisor=UserFactory.create(CustomUser.SUPERVISOR),
            case_number=fake.uuid4()[:8],
            cr_number=fake.uuid4()[:8],
            arraignment_date=fake.date(),
            judge=JudgeFactory.create(),
            defense_attorney=DefenseAttorneyFactory.create(),
            defendant=DefendantFactory.create(),
        )
