"""
账户认证接口单元测试(示例 + 冒烟测试)。

运行方式::

    python manage.py test --settings=Backend.settings.unittest

本测试使用内存 SQLite(见 settings/unittest.py),不连接任何 MySQL / Redis,
既验证认证五链路可用,也作为编写后续业务测试的范式参考。

要点:
- 继承 DRF ``APITestCase``,用 ``self.client`` 发起请求;
- 所有响应断言统一结构 ``{code, message, data, requestId}``;
- 每个测试方法独立、互不依赖,数据库在每个用例后自动回滚。
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class AuthApiTests(APITestCase):
    """认证接口:注册 / 登录 / 当前用户 / 刷新 / 登出。"""

    def setUp(self):
        self.register_url = "/auth/registration/"
        self.login_url = "/auth/login/"
        self.user_url = "/auth/user/"
        self.logout_url = "/auth/logout/"
        self.refresh_url = "/auth/token/refresh/"

    # ── 通用断言:响应为统一结构且业务码符合预期 ──
    def assertEnvelope(self, response, expect_code=200):
        body = response.json()
        self.assertIn("code", body)
        self.assertIn("message", body)
        self.assertIn("data", body)
        self.assertIn("requestId", body)
        self.assertEqual(body["code"], expect_code)
        return body

    def _register(self, username="alice", password="secret123"):
        return self.client.post(
            self.register_url,
            {
                "username": username,
                "email": f"{username}@example.com",
                "password1": password,
                "password2": password,
            },
            format="json",
        )

    # ── 注册 ──

    def test_register_success(self):
        """注册成功返回令牌对与用户信息。"""
        resp = self._register()
        body = self.assertEnvelope(resp, 200)
        self.assertIn("access_token", body["data"])
        self.assertIn("refresh_token", body["data"])
        self.assertEqual(body["data"]["user"]["username"], "alice")
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_password_mismatch(self):
        """两次密码不一致返回 400。"""
        resp = self.client.post(
            self.register_url,
            {
                "username": "bob",
                "email": "bob@example.com",
                "password1": "secret123",
                "password2": "different",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    # ── 登录 ──

    def test_login_success(self):
        """正确用户名密码登录成功。"""
        self._register(username="carol")
        resp = self.client.post(
            self.login_url, {"username": "carol", "password": "secret123"}, format="json"
        )
        body = self.assertEnvelope(resp, 200)
        self.assertIn("access_token", body["data"])

    def test_login_wrong_password(self):
        """密码错误返回 400。"""
        self._register(username="dave")
        resp = self.client.post(
            self.login_url, {"username": "dave", "password": "wrong"}, format="json"
        )
        self.assertEqual(resp.status_code, 400)

    # ── 当前用户 / 鉴权 ──

    def test_current_user_with_token(self):
        """带 access token 可获取当前用户。"""
        access = self._register(username="erin").json()["data"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        resp = self.client.get(self.user_url)
        body = self.assertEnvelope(resp, 200)
        self.assertEqual(body["data"]["username"], "erin")

    def test_current_user_without_token(self):
        """未带 token 访问返回 401。"""
        resp = self.client.get(self.user_url)
        self.assertEqual(resp.status_code, 401)

    # ── 刷新 ──

    def test_refresh_token(self):
        """refresh token 可续签新 access。"""
        refresh = self._register(username="frank").json()["data"]["refresh_token"]
        resp = self.client.post(self.refresh_url, {"refresh_token": refresh}, format="json")
        body = self.assertEnvelope(resp, 200)
        self.assertIn("access_token", body["data"])

    # ── 登出使历史令牌失效 ──

    def test_logout_invalidates_token(self):
        """登出后旧 access token 立即失效(token_version 递增)。"""
        access = self._register(username="grace").json()["data"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        # 登出成功
        self.assertEqual(self.client.post(self.logout_url).status_code, 200)
        # 旧 token 再访问应 401
        resp = self.client.get(self.user_url)
        self.assertEqual(resp.status_code, 401)
