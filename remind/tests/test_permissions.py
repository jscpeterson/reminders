from django.test import TestCase
from remind.tests.factories import UserFactory, CaseFactory
from django.urls import reverse
from guardian.shortcuts import assign_perm


class CasePerObjectDetailViewPermissionsTest(TestCase):
    """
    Case permissions can be managed on a per-object basis. This test case
    ensures those per-object permissions work correctly.
    """

    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)

        self.case = CaseFactory.create()
        self.url = reverse('remind:update', kwargs={'case_number': self.case.case_number})

    def test_view_as_regular_user(self):
        """ By default regular users don't have access to any cases. """
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_view_as_regular_user_with_permission(self):
        """
        When granted permission regular users can have access to specific
        cases.
        """
        assign_perm('change_case', self.user, self.case)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_user_cant_access_not_allowed_object(self):
        another_case = CaseFactory.create()

        # user has access to `another_case` but not the one from the url
        assign_perm('change_case', self.user, another_case)

        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)
