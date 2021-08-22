from classroom.views import course_detail
from assignment.views import delete_assignment
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from django.test import TestCase
from django.test.client import RequestFactory

from classroom.models import Course, Category, Module

from .views import delete_module, new_module

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

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        new_module(req, self.course.id)
        module = Module.objects.get(title=info['title'])
        assert module
        return module

    def test_del_module(self):
        mod = ModuleTest.test_new_module(self)
        mod_id = mod.id
        req = self.factory.post(f'{self.course.id}/modules/{mod_id}/delete')
        req.user = self.user
        delete_module(req,self.course.id,mod.id)
        try:
            mod=Module.objects.get(id=mod_id)
            assert False
        except Exception:
            assert True
    
    def test_cour_mod(self):
        mod = ModuleTest.test_new_module(self)
        mod_id = mod.id
        req = self.factory.get('module/modules.html')
        req.user = self.user
        course_detail(req,self.course.id)
        mod01=Module.objects.get(id=mod_id)
        assert mod01