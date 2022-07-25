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
            data={"username": "test_user1", "password1": "12345678", "password2": "12345678"}
        )
        self.assertEqual(res.status_code, 201)

    def test_exsist_username(self):
        res = self.client.post(
            path="/api/v1/users/",
            data={"username": "user1", "password1": "12345678", "password2": "12345678"}
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_password_1_2_not_same(self):
        res = self.client.post(
            path="/api/v1/users/",
            data={"username": "test_user1", "password1": "12345678", "password2": "12345677"}
        )
        self.assertEqual(res.status_code, 400)

    def test_change_user_password(self):
        self.test_user_create()
        user = User.objects.get(username="test_user1")
        token = Token.objects.get(user_id=user.id)
        headers = {'HTTP_AUTHORIZATION': f"Token {token}"}

        res = self.client.patch(
            path=f"/api/v1/users/{user.id}/",
            data={"old_password": "12345678", "new_password": "123123123", "confirm_password": "123123123"},
            content_type="application/json",
            **headers
        )
        self.assertEqual(res.status_code, 200)

    def test_change_user_password_failed(self):
        self.test_user_create()
        user = User.objects.get(username="test_user1")
        token = Token.objects.get(user_id=user.id)
        headers = {'HTTP_AUTHORIZATION': f"Token {token}"}

        # CASE1.
        res = self.client.patch(
            path=f"/api/v1/users/{user.id}/",
            data={"old_password": "12345677", "new_password": "123123123", "confirm_password": "123123123"},
            content_type="application/json",
            **headers
        )
        self.assertEqual(res.status_code, 400)

        # CASE2.
        res = self.client.patch(
            path=f"/api/v1/users/{user.id}/",
            data={"old_password": "12345678", "new_password": "12312312", "confirm_password": "123123123"},
            content_type="application/json",
            **headers
        )
        self.assertEqual(res.status_code, 400)

        # CASE3.
        fake_user = User.objects.get(id=self.User1.id)
        fake_token = Token.objects.get(user_id=fake_user.id)
        fake_headers = {'HTTP_AUTHORIZATION': f"Token {fake_token}"}

        res = self.client.patch(
            path=f"/api/v1/users/{user.id}/",
            data={"old_password": "12345678", "new_password": "123123123", "confirm_password": "123123123"},
            content_type="application/json",
            **fake_headers
        )
        self.assertEqual(res.status_code, 403)

    # 유저 삭제 성공

    # 유저 삭제 실패
