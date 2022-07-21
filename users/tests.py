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

    # 유저 비밀번호 수정 성공

    # 유저 비밀번호 수정 실패

    # 유저 삭제 성공

    # 유저 삭제 실패