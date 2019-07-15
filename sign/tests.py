from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from sign.models import Event, Guest


class ModelTest(TestCase):
    # 模型测试
    def setUp(self):
        Event.objects.create(id=1, name='ok one', status=True, limit=1500, address='hangzhou', start_time='2019-06-20')
        Guest.objects.create(id=1, event_id=1, realname='KK', phone='13898453657', email='kk@example.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='ok one')
        self.assertEqual(result.address, 'hangzhou')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13898453657')
        self.assertEqual(result.realname, 'KK')
        self.assertFalse(result.sign)


# 视图测试
class IndexPageTest(TestCase):
    """
    测试Index登录首页
    """

    def test_index_page_renders_index_template(self):
        """
        测试视图
        :return:
        """
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        # 判定服务是是否用给定的模板作为响应
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    """
    测试登录动作
    """

    def setUp(self):
        User.objects.create_user('ha', email='ha@example', password='1234')

    def test_add_user(self):
        """
        添加用户测试
        """
        user = User.objects.get(username='ha')
        self.assertEqual(user.username, 'ha')
        self.assertEqual(user.email, 'ha@example')

    def test_login_action_username_password_null(self):
        """
        用户名密码为空
        :return:
        """
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_username_password_error(self):
        """
        用户名密码错误
        :return:
        """
        test_data = {'username': 'ah', 'password': '321'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)


    def test_login_action_success(self):
        """
        登录成功
        :return:
        """
        test_data = {'username': 'ha', 'password': '1234'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """
    发布会管理测试
    """

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', '1234')
        Event.objects.create(name='one two', limit=1024, address='beijing', status=1, start_time='2019-07-30')
        self.login_user = {'username': 'admin', 'password': '1234'}

    def test_event_manage_success(self):
        """
        测试发布会 one two
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'one two', response.content)
        self.assertIn(b'beijing', response.content)

    def test_event_manage_search_success(self):
        """
        测试发布会搜索
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {'name': 'one two'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'one two', response.content)
        self.assertIn(b'beijing', response.content)

class GuestManageTest(TestCase):
    """
    嘉宾管理测试
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', '1234')
        Event.objects.create(id=1, name='one two', limit=1024, address='beijing', status=1, start_time='2019-07-30')
        Guest.objects.create(id=1, event_id=1, realname='kk', phone='13800001111', email='kk@example.com', sign=False)
        self.login_user = {'username': 'admin', 'password': '1234'}

    def test_event_manage_success(self):
        """
        测试嘉宾信息 kk
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'kk', response.content)
        self.assertIn(b'13800001111', response.content)

    def test_guest_manage_search_success(self):
        """
        测试嘉宾搜索
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_guest/', {'name': '13800001111'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'kk', response.content)
        self.assertIn(b'13800001111', response.content)

class SignIndexActionTest(TestCase):
    """
    发布会签到测试
    """
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', '1234')
        Event.objects.create(id=1, name='one two', limit=1024, address='beijing', status=1, start_time='2019-07-30')
        Guest.objects.create(id=1, event_id=1, realname='kk', phone='13800001111', email='kk@example.com', sign=0)
        Event.objects.create(id=2, name='three four', limit=100, address='hangzhou', status=1, start_time='2019-07-30')
        Guest.objects.create(id=2, event_id=2, realname='jj', phone='13822221111', email='jj@example.com', sign=1)
        self.login_user = {'username': 'admin', 'password': '1234'}

    def test_sign_index_action_phone_null(self):
        """
        手机号为空
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Phone Error.', response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        """
        手机号或发布会id错误
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '13800001111'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event id or phone error.', response.content)

    def test_sign_index_action_user_had_signed(self):
        """
        用户已签到
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '13822221111'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user had signed.', response.content)

    def test_sign_index_action_sign_success(self):
        """
        签到成功
        :return:
        """
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': '13800001111'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success.', response.content)