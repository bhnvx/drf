from test_plus.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        # User
        self.AdminUser = User.objects.create(username="admin", is_staff=True, is_superuser=True)
        self.User1 = User.objects.create(username="user1")
        self.User2 = User.objects.create(username="user2")

    def admin_test(self):
        self.client.force_login(self.AdminUser)

        res = self.client.post(
            path="",
            data={},
            content_type=""
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIsNotNone(data["id"])

        user = User.objects.get(id=data["id"])
