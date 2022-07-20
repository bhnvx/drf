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

    def test_admin_get_user(self):
        self.client.force_login(self.AdminUser)
        token = Token.objects.get(user_id=self.AdminUser.id)
        headers = {'HTTP_AUTHORIZATION': f"Token {token}"}

        res = self.client.get(
            path="/api/v1/users/",
            **headers
        )

        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsNotNone(data)
        quesryset = User.objects.all()
        self.assertEqual(len(data), len(quesryset))

        for query in quesryset:
            res = self.client.get(
                path=f"/api/v1/users/{query.id}",
                **headers
            )
            self.assertRedirects(res, f"/api/v1/users/{query.id}/", status_code=301, target_status_code=200)

    def test_not_admin_get_user(self):
        self.client.force_login(self.User1)
        token = Token.objects.get(user_id=self.User1.id)
        headers = {'HTTP_AUTHORIZATION': f"Token {token}"}

        res = self.client.get(
            path="/api/v1/users/",
            **headers
        )
        self.assertEqual(res.status_code, 403)

        pk = User.objects.get(id=self.User2.id).id
        res = self.client.get(
            path=f"/api/v1/users/{pk}",
            **headers
        )
        self.assertRedirects(res, f"/api/v1/users/{pk}/", status_code=301, target_status_code=403)

    def test_user_create(self):
        res = self.client.post(
            path="/api/v1/users/",
            data={"username": None, "password1": None, "password2": None}
        )