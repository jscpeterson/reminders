from django.test import TestCase
from datetime import datetime, timedelta
from pytz import timezone
from django.conf import settings
from remind.models import Case
from users.models import CustomUser
from remind.forms import SchedulingForm
from . import utils


class TestSchedulingForm(TestCase):

    def test_valid_data(self):
        users = utils.create_test_users()
        positions = CustomUser.get_positions_dict()

        case = Case.objects.create(
            case_number='0001',
            paralegal=users[positions[CustomUser.PARALEGAL]],
            prosecutor=users[positions[CustomUser.PROSECUTOR]],
            supervisor=users[positions[CustomUser.SUPERVISOR]],
            arraignment_date=datetime.now(tz=timezone(settings.TIME_ZONE)),
        )
        form = SchedulingForm(
            {'scheduling_conference_date': case.arraignment_date + timedelta(days=1)},
            case_number=case.case_number,
        )
        self.assertTrue(form.is_valid())
