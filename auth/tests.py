from test_plus.test import TestCase
from rest_framework.authtoken.models import Token
from users.models import Users as User
from users.tests import UserTestCase


class AuthTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.User1 = User.objects.create(username="user1")

    def test_user_info(self):
        self.client.force_login(self.User1)
        token = Token.objects.get(user_id=self.User1.id)
        headers = {'HTTP_AUTHORIZATION': f"Token {token}"}

        res = self.client.get(
            path="/api/v1/auth/me",
            **headers
        )
        self.assertRedirects(res, "/api/v1/auth/me/", status_code=301, target_status_code=200)

    def test_user_login(self):
        UserTestCase.test_user_create(self)
        user = User.objects.get(username="test_user1")

        res = self.client.post(
            path="/api/v1/auth/login/",
            data={"username": user.username, "password": "12345688"},
        )
        self.assertEqual(res.status_code, 400)

        res = self.client.post(
            path="/api/v1/auth/login/",
            data={"username": user.username, "password": "12345678"},
        )
        self.assertEqual(res.status_code, 200)
