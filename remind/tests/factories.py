from faker import Faker
from random import randint

from remind.constants import JUDGES
from cases.models import Case
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
            arraignment_date=fake.date(),
            judge=JUDGES[randint(0, len(JUDGES)-1)][1],
            defendant=fake.first_name() + ' ' + fake.last_name(),
        )
