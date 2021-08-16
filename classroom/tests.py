from django.test import TestCase
from .models import Category, Course, Grade
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import delete_course, new_course, edit_course, enroll, delete_course
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

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
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
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

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        new_course(req)

        course = Course.objects.get(title = 'English')
        assert course
        return course

    def test_edit_course(self):
        course = CourseTest.test_new_course(self)
        course_id = course.id
        req = self.factory.post(f'course/{course_id}/edit')
        req.user = self.user
        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'Español',
                'category': self.category.id,
                'day': 'JU',
                'description': 'Curso basico, intermedio, avanzado de Español',
                'time_start': '14:00:00',
                'time_end': '17:30:00',
                'syllabus': 'syllabus test 2',
                'action': ''
                }
        
        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        edit_course(req,course_id)
        course = Course.objects.get(title = 'Español')
        assert course

    def test_enroll(self):
        course = CourseTest.test_new_course(self)
        course_id = course.id
        req = self.factory.post(f'course/{course_id}/enroll')
        req.user = self.user
        enroll(req,course_id)

        for user_enrolled in course.enrolled.all():
            if user_enrolled.id == self.user.id:
                assert True
            else:
                assert False

    def test_delete_course(self):
        course = CourseTest.test_new_course(self)
        course_id = course.id
        req = self.factory.post(f'course/{course_id}/delete')
        req.user = self.user
        delete_course(req,course_id)
        try:
            course = Course.objects.get(id = course_id)
            assert False
        except:
            assert True
        
    

    
        

