# -*- coding: utf8 -*-
import unittest


class TestAccountView(unittest.TestCase):
    def setUp(self):
        from .helper import init_testing_env
        self.testapp = init_testing_env({
            'sqlalchemy.write.url': 'sqlite:///',
            'use_dummy_mailer': True
        })
        self.create_testuser()
        
    def tearDown(self):
        self.testapp.Session.remove()
        
    def create_testuser(self):
        import transaction
        from ..models.user import UserModel
        model = UserModel(self.testapp.session)
        with transaction.manager:
            model.create_user(
                user_name='tester', 
                display_name='tester', 
                password='testerpass', 
                email='tester@example.com'
            )
        
    def login_user(self, username_or_email='tester', password='testerpass'):
        """Login as user and return cookie
        
        """
        params = dict(
            username_or_email=username_or_email, 
            password=password
        )
        self.testapp.post('/login', params)
        
    def assert_login_success(self, name, password):
        """Assert login success
        
        """
        params = dict(
            username_or_email=name, 
            password=password
        )
        self.testapp.post('/login', params, status='3*')
        
    def assert_login_failed(self, name, password):
        """Assert login failed
        
        """
        params = dict(
            username_or_email=name, 
            password=password
        )
        self.testapp.post('/login', params, status=200)
        
    def test_login(self):
        self.testapp.get('/login', status=200)
        # test valid login
        self.assert_login_success('tester', 'testerpass')
        self.assert_login_success('TESTER', 'testerpass')
        self.assert_login_success('TeStEr', 'testerpass')
        self.assert_login_success('tester@example.com', 'testerpass')
        self.assert_login_success('TESTER@example.com', 'testerpass')
        self.assert_login_success('TESTER@Example.Com', 'testerpass')
        
    def test_login_fail(self):
        self.testapp.get('/login', status=200)
        
        with self.assertRaises(Exception):
            self.assert_login_failed('tester', 'testerpass')
        
        # test invalid login
        self.assert_login_failed('', '')
        self.assert_login_failed('tester', 'tester')
        self.assert_login_failed('tester', 'TESTERPASS')
        self.assert_login_failed('tester', 'TeStErPaSs')
        self.assert_login_failed('tester@example.com', 'tester')
        self.assert_login_failed('tester@example.com', 'TESTERPASS')
        self.assert_login_failed('tester@example.com', 'TeStErPaSs')
        self.assert_login_failed('tester', '')
        self.assert_login_failed('tester@example.com', '')
        self.assert_login_failed('abc', '123')
        self.assert_login_failed('not_exist@example.com', '123')
        self.assert_login_failed('not_exist@example.com', '')
        
    def test_logout(self):
        # try to logout when not logged in
        self.testapp.get('/logout', status=400)
        self.login_user('tester', 'testerpass')
        self.testapp.get('/logout', status='3*')

    def test_recovery_password(self):
        self.testapp.get('/forgot_password', status=200)

        res = self.testapp.post('/forgot_password', dict(
            email='tester@example.com',
        ), status=200)
        mailer = res.request.environ['pyramid_mailer.dummy_mailer']
        self.assertEqual(len(mailer.outbox), 1)
        mail = mailer.outbox[0]
        # find recovery link
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(mail.html)
        links = soup.findAll('a')
        recovery_link = None
        for link in links:
            if 'recovery_password' in link['href']:
                recovery_link = link['href']
                break

        self.testapp.get('/recovery_password?user_name=xxx&code=xxx', status=404)
        self.testapp.get('/recovery_password?user_name=tester&code=xxx', status=403)
        self.testapp.get(recovery_link, status=200)

        import urlparse
        import urllib
        q = urlparse.parse_qs(recovery_link.split('?')[-1])

        code = q['code'][0]
        qs = q.copy()
        qs.update(dict(code=code + '0'))
        qs = urllib.urlencode(qs, True)
        self.testapp.get('/recovery_password?' + qs, status=403)

        qs = q.copy()
        qs.update(dict(user_name='tester01'))
        qs = urllib.urlencode(qs, True)
        self.testapp.get('/recovery_password?' + qs, status=404)

        self.testapp.get(recovery_link, status=200)
        self.testapp.post(recovery_link, dict(
            new_password_confirm='password1',
            new_password='password2',
        ), status=200) 
        # make sure the password is not changed
        self.assert_login_success('tester', 'testerpass')

        self.testapp.post(recovery_link, dict(
            new_password_confirm='newpass',
            new_password='newpass',
        ), status=302) 
        # make sure the password is not changed
        self.assert_login_success('tester', 'newpass')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAccountView))
    return suite
        
if __name__ == '__main__':
    unittest.main(defaultTest='suite')
