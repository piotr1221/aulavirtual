from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from django.test import TestCase
from django.test.client import RequestFactory

from classroom.models import Course, Category, Module

from .views import new_module

# Create your tests here.
class ModuleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='xocrona',
                                            email='xocrona@xocrona.com',
                                            password='xocrona',
                                            )
        self.category = Category.objects.create(title='test_category',
                                            icon='test_icon',
                                            slug='test-category'
                                            )
        self.course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocrona',
                                            day='LU',
                                            time_start='10:00',
                                            time_end='11:00',
                                            category=Category.objects.get(id=self.category.id),
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )

    def test_new_module(self):
        req = self.factory.post('newcourse')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'new_title',
                'hours': 1,
                }

        #middleware = SessionMiddleware()
        #middleware.process_request(req)
        #req.session.save()

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        new_module(req, self.course.id)
        module = Module.objects.get(title=info['title'])
        assert module