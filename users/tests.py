from test_plus.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

    # ...