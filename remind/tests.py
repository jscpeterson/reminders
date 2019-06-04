from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from . import utils
from .constants import LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND
from .models import Deadline, Case
from users.models import CustomUser


class TestActualDeadline(TestCase):

    def test_long_deadline_from_start(self):
        # Test cases of 60 day deadlines
        # Deadline from test case T-4-FR-2019000277
        event = datetime(2019, 1, 18, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Date of preventive detention
        days = 60
        result = datetime(2019, 3, 19, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # 60 day deadline for arraignment
        self.assertEqual(utils.get_actual_deadline_from_start(event, days), result)

        # Deadline from test case T-4-FR-2018004144
        event = datetime(2018, 8, 2, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Date of preventive detention
        days = 60
        result = datetime(2018, 10, 1, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # 60 day deadline for arraignment
        self.assertEqual(utils.get_actual_deadline_from_start(event, days), result)

    def test_weekend_deadline_from_start(self):
        # Test case in which a 10 day deadline overlapped with a weekend, but no holidays
        # Deadline from test case T-4-FR-2018004144
        event = datetime(2018, 8, 2, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Date of preventive detention
        days = 10
        result = datetime(2018, 8, 16, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # 10 day deadline for arraignment
        self.assertEqual(utils.get_actual_deadline_from_start(event, days), result)

    def test_holiday_deadline_from_start(self):
        # Test case in which a 10 day deadline overlapped with weekends and a holiday, deadline landing on a weekend
        # Deadline from test case T-4-FR-2019000277
        event = datetime(2019, 1, 18, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Date of preventive detention
        days = 10
        result = datetime(2019, 2, 4, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # 10 day deadline for arraignment
        self.assertEqual(utils.get_actual_deadline_from_start(event, days), result)

    def test_long_deadline_from_end(self):
        # Test case of 15 day deadline from end date event
        # Using status hearing of D-202-CR-2019-00568 as reference
        event = datetime(2019, 10, 21, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Date of trial
        days = 15
        result = datetime(2019, 10, 4, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Latest possible deadline for witness list/language access services
        self.assertEqual(utils.get_actual_deadline_from_end(event, days), result)

    def test_holiday_deadline_from_end(self):
        # Test case of 10 day deadline from end date event, overlapping with weekends and holidays
        # Using status hearing of D-202-CR-2019-00568 as reference
        event = datetime(2019, 10, 21, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Date of trial
        days = 10
        result = datetime(2019, 10, 4, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)  # Latest possible deadline for submitting a plea deal
        self.assertEqual(utils.get_actual_deadline_from_end(event, days), result)


class TestDeadlineCheck(TestCase):

    def test_long_prior_event(self):
        event = datetime(2018, 8, 2, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        days = 60
        deadline = datetime(2018, 10, 1, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        good_deadline = datetime(2018, 10, 2, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        bad_deadline = datetime(2018, 9, 28, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        self.assertTrue(utils.is_deadline_within_limits(deadline=deadline, event=event, days=days, future_event=False))
        self.assertTrue(utils.is_deadline_within_limits(deadline=good_deadline, event=event, days=days, future_event=False))
        self.assertFalse(utils.is_deadline_within_limits(deadline=bad_deadline, event=event, days=days, future_event=False))

    def test_10day_prior_event(self):
        event = datetime(2018, 8, 2, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        days = 10
        deadline = datetime(2018, 8, 16, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        good_deadline = datetime(2018, 8, 17, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        bad_deadline = datetime(2018, 8, 15, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        self.assertTrue(utils.is_deadline_within_limits(deadline=deadline, event=event, days=days, future_event=False))
        self.assertTrue(utils.is_deadline_within_limits(deadline=good_deadline, event=event, days=days, future_event=False))
        self.assertFalse(utils.is_deadline_within_limits(deadline=bad_deadline, event=event, days=days, future_event=False))

    def test_long_future_event(self):
        event = datetime(2019, 10, 21, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        days = 15
        deadline = datetime(2019, 10, 4, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        good_deadline = datetime(2019, 10, 3, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        bad_deadline = datetime(2019, 10, 7, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        self.assertTrue(utils.is_deadline_within_limits(deadline=deadline, event=event, days=days, future_event=True))
        self.assertTrue(utils.is_deadline_within_limits(deadline=good_deadline, event=event, days=days, future_event=True))
        self.assertFalse(utils.is_deadline_within_limits(deadline=bad_deadline, event=event, days=days, future_event=True))

    def test_10day_future_event(self):
        event = datetime(2019, 10, 21, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        days = 10
        deadline = datetime(2019, 10, 4, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        good_deadline = datetime(2019, 10, 3, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        bad_deadline = datetime(2019, 10, 7, LAST_DAY_HOUR, LAST_DAY_MINUTE, LAST_DAY_SECOND)
        self.assertTrue(utils.is_deadline_within_limits(deadline=deadline, event=event, days=days, future_event=True))
        self.assertTrue(utils.is_deadline_within_limits(deadline=good_deadline, event=event, days=days, future_event=True))
        self.assertFalse(utils.is_deadline_within_limits(deadline=bad_deadline, event=event, days=days, future_event=True))


class TestExtensionCheck(TestCase):

    def setUp(self):
        self.paralegal = CustomUser.objects.create(
            first_name='Bart',
            last_name='Simpson',
            position=CustomUser.PARALEGAL,
            username='plegal',
        )
        self.prosecutor = CustomUser.objects.create(
            first_name='Lionel',
            last_name='Hutz',
            position=CustomUser.PROSECUTOR,
            username='lawyerman123',
        )
        self.supervisor = CustomUser.objects.create(
            first_name='Montgomery',
            last_name='Burns',
            position=CustomUser.SUPERVISOR,
            username='supervisor001',
        )

    def test_trial_deadline(self):
        case = Case.objects.create(
            arraignment_date=datetime(2019, 1, 11),
            track=1,
            paralegal=self.paralegal,
            prosecutor=self.prosecutor,
            supervisor=self.supervisor,
        )
        good_deadline = Deadline.objects.create(
            type=Deadline.TRIAL,
            datetime=datetime(2019, 7, 8),
            case=case,
        )
        invalid_deadline = Deadline.objects.create(
            type=Deadline.TRIAL,
            datetime=datetime(2019, 9, 10),
            case=case,
        )
        extension_deadline = Deadline.objects.create(
            type=Deadline.TRIAL,
            datetime=datetime(2019, 8, 21),
            case=case,
        )
        self.assertFalse(utils.is_extension_required(good_deadline))
        self.assertTrue(utils.is_extension_required(extension_deadline))
        self.assertFalse(utils.is_extension_required(invalid_deadline))

    def test_scientific_deadline(self):
        case = Case.objects.create(
            trial_date=datetime(2019, 6, 3),
            track=2,
            paralegal=self.paralegal,
            prosecutor=self.prosecutor,
            supervisor=self.supervisor,
        )
        good_deadline = Deadline.objects.create(
            type=Deadline.SCIENTIFIC_EVIDENCE,
            datetime=datetime(2019, 2, 1),
            case=case,
        )
        invalid_deadline = Deadline.objects.create(
            type=Deadline.SCIENTIFIC_EVIDENCE,
            datetime=datetime(2019, 4, 1),
            case=case,
        )
        extension_deadline = Deadline.objects.create(
            type=Deadline.SCIENTIFIC_EVIDENCE,
            datetime=datetime(2019, 2, 10),
            case=case,
        )
        self.assertFalse(utils.is_extension_required(good_deadline))
        self.assertTrue(utils.is_extension_required(extension_deadline))
        self.assertFalse(utils.is_extension_required(invalid_deadline))


class TestInvalidDeadlineCheck(TestCase):

    def setUp(self):
        self.paralegal = CustomUser.objects.create(
            first_name='Bart',
            last_name='Simpson',
            position=CustomUser.PARALEGAL,
            username='plegal',
        )
        self.prosecutor = CustomUser.objects.create(
            first_name='Lionel',
            last_name='Hutz',
            position=CustomUser.PROSECUTOR,
            username='lawyerman123',
        )
        self.supervisor = CustomUser.objects.create(
            first_name='Montgomery',
            last_name='Burns',
            position=CustomUser.SUPERVISOR,
            username='supervisor001',
        )

    def test_scheduling_conference(self):
        case = Case.objects.create(
            arraignment_date=datetime(2019, 1, 11),
            track=1,
            paralegal=self.paralegal,
            prosecutor=self.prosecutor,
            supervisor=self.supervisor,
        )
        good_deadline = Deadline.objects.create(
            type=Deadline.SCHEDULING_CONFERENCE,
            datetime=datetime(2019, 2, 8),
            case=case,
        )
        invalid_deadline = Deadline.objects.create(
            type=Deadline.SCHEDULING_CONFERENCE,
            datetime=datetime(2019, 2, 12),
            case=case,
        )
        self.assertFalse(utils.is_deadline_invalid(good_deadline))
        self.assertTrue(utils.is_deadline_invalid(invalid_deadline))

    def test_trial_deadline(self):
        case = Case.objects.create(
            trial_date=datetime(2019, 6, 3),
            track=1,
            paralegal=self.paralegal,
            prosecutor=self.prosecutor,
            supervisor=self.supervisor,
        )
        good_deadline = Deadline.objects.create(
            type=Deadline.FINAL_WITNESS_LIST,
            datetime=datetime(2019, 5, 17),
            case=case,
        )
        invalid_deadline = Deadline.objects.create(
            type=Deadline.FINAL_WITNESS_LIST,
            datetime=datetime(2019, 5, 24),
            case=case,
        )
        self.assertFalse(utils.is_deadline_invalid(good_deadline))
        self.assertTrue(utils.is_deadline_invalid(invalid_deadline))
