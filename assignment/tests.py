from module.models import Module
from django.contrib.messages.storage.fallback import FallbackStorage
from classroom.models import Category, Course
from django.test import TestCase
from .models import Assignment
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import new_assignment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

class CourseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='xocrona',
                                            email='xocrona@xocrona.com',
                                            password='xocrona',
                                            )
        self.category = Category.objects.create(title='Idiomas',
                                                        icon='noicon',
                                                        slug='test',
                                                        )
        self.course = Course.objects.create(picture= None,
                                                        title= 'English',
                                                        description= 'Basic Intermediate Advance English course',
                                                        day= 'LU',
                                                        time_start= '12:00:00',
                                                        time_end ='14:30:00',
                                                        category= self.category,
                                                        syllabus= 'syllabus test',
                                                        user=self.user)
        self.module = Module.objects.create(title = 'test',
	                                                    user = self.user,
	                                                    hours = 3,	
                                                        )
        

    
    def test_new_ass(self):

        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/assignment/newassignment')

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'test',
	            'content': 'test',
	            'points': 10,
	            'due': '10/08/2021',
	            'files': None,
                }

        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q
        req.user = self.user

        #m = MultiValueDict('')
        #m.appendlist(file_data)
        #print(type(req.FILES))
        #req.FILES = m
        

        new_assignment(req,self.course.id,self.module.id)

        ass01 = Assignment.objects.get(title = 'test')
        assert ass01


