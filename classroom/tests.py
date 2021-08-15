from django.test import TestCase
from .models import Category, Course, Grade
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import new_course
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
#import urllib
#from django.core.files.uploadedfile import SimpleUploadedFile
#from PIL import Image
#from django.utils.datastructures import MultiValueDict
# Create your tests here.

class CourseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(title='Idiomas',
                                                        icon='noicon',
                                                        slug='test',
                                                        )
        self.user = User.objects.create_user(username='xocrona',
                                            email='xocrona@xocrona.com',
                                            password='xocrona',
                                            )
        

    def test_new_course(self):
        req = self.factory.post('course/newcourse')
        

        #result = urllib.urlopen('https://static.wikia.nocookie.net/nekos-judios/images/1/17/Xocron-_digo_digo%2C_el_tio_anthony.jpg/revision/latest/top-crop/width/360/height/450?cb=20180624223121&path-prefix=es')
        #im = Image.open("D:\Alexis\Projects in programming\Project in Phyton\django projects\aulavirtual\media\user_1\profile.jpg")
        #buf = BytesIO()
        #im.save(buf, format='JPEG')
        #byte_im = buf.getvalue()
        #file_data = {'profile': SimpleUploadedFile('profile.jpg', byte_im)}
        
        
        info = {'csrfmiddlewaretoken': get_token(req),
                'picture': None,
                'title': 'English',
                'category': self.category.id,
                'day': 'LU',
                'description': 'Basic Intermediate Advance English course',
                'time_start': '12:00:00',
                'time_end': '14:30:00',
                'syllabus': 'syllabus test',
                'action': ''
                }

        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        user = User.objects.create_user('test_user', 'test_user@gmail.com', 'test_user')

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q
        req.user = user

        #m = MultiValueDict('')
        #m.appendlist(file_data)
        #print(type(req.FILES))
        #req.FILES = m
        

        new_course(req)

        course = Course.objects.get(title = 'English')
        assert course





