from django.test import TestCase
from .models import Profile
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import password_change_done, side_nav_info, signup, edit_profile, password_change, user_profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# Create your tests here.

class ProfileTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='xocrona',
                                            email='xocrona@xocrona.com',
                                            password='xocrona',
                                            )

    def test_register(self):
        req = self.factory.post('user/signup')

        info = {'csrfmiddlewaretoken': get_token(req),
                'username': 'test_user',
                'email': 'test_user@gmail.com',
                'password': 'test_user',
                'confirm_password': 'test_user',
                'action': '',
                }

        user = User.objects.create_user('test_user', 'test_user@gmail.com', 'test_user')

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q
        req.user = user
        signup(req)
        user = User.objects.get(username='test_user')
        assert user

    def test_edit_profile(self):
        req = self.factory.post('user/profile/edit')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'first_name': 'test',
                'last_name': 'user',
                'location': 'test location',
                'url': 'testurl.com',
                'profile_info': 'test profile info',
                'action': '',
                }

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        edit_profile(req)
        profile = Profile.objects.get(user=self.user)
        assert profile.location

    def test_change_password(self):
        req = self.factory.post('user/changepassword')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'id': req.user.id,
                'old_password': 'xocrona',
                'new_password': 'new_xocrona',
                'confirm_password': 'new_xocrona',
                }

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        password_change(req)
        user = User.objects.get(username=self.user.username)
        assert user.check_password(info['new_password'])
        return user

    def test_side(self):
        req = self.factory.post('login')
        req.user = self.user
        side_nav_info(req)
        user = User.objects.get(username=self.user)
        assert user

    '''def test_profile(self):
        req = self.factory.post(f'{self.user.username}')
        req.user = self.user
        user_profile(req,self.user.username)
        user=User.objects.get(email='xocrona@xocrona.com')
        assert user'''

    def test_change_pass_done(self):

        #us = ProfileTest.test_change_password(self)
        #us_username = us.username
        req = self.factory.get('user/changepassword/done')
        req.user = self.user

        password_change_done(req)
        user01 = User.objects.get(username=self.user)
        assert user01
