from test_plus.test import TestCase
from rest_framework.authtoken.models import Token
from users.models import Users as User


class UserTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        # User
        self.AdminUser = User.objects.create(username="admin", is_staff=True, is_superuser=True)
        self.User1 = User.objects.create(username="user1")
        self.User2 = User.objects.create(username="user2")

        # URL Path
        self.url = "/api/v1/"

    def test_admin_get_all_user(self):
        self.client.force_login(self.AdminUser)
        token = Token.objects.get(user_id=User.objects.get(username="admin").id)
        headers = {'HTTP_AUTHORIZATION': f"Token {token}"}

        res = self.client.get(
            path="/api/v1/users/",
            **headers
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsNotNone(data)
