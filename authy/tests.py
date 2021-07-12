from django.test import TestCase
from .models import Profile
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import Signup
# Create your tests here.

class ProfileTest(TestCase):

    def test_register(self):
        req = WSGIRequest({"PATH_INFO": "/user/signup", "REQUEST_METHOD": "post", "wsgi.input": BytesIO(b"")})
        info = {'csrfmiddlewaretoken': get_token(req), 'username': 'dsa3', 'email': 'dsa2@gmail.com', 'password': '123', 'confirm_password': '123', 'action': ''}
        #print(req)
        
        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q
        #print(get_token(req))
        Signup(req)