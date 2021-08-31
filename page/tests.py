
from page.models import Page
from page.views import delete_page, mark_page_as_done, new_page_module, page_detail
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from module.models import Module
from django.contrib.auth.models import User
from classroom.models import Category, Course, Grade
from django.test import TestCase
from django.test.client import RequestFactory


class PageTest(TestCase):
    # metodo setup
    # establece valores
    # iniciales que se utilizaran
    # en la suite de tests
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

        self.course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocrona',
                                            day='1',
                                            time_start='10:00',
                                            time_end='11:00',
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )
        self.student = User.objects.create_user(username='xocronakbro',
                                            email='xocrona@soymaricon.com',
                                            password='xocronakbro',
                                            )
        self.grade = Grade.objects.create(course = self.course,
                                        student = self.student,
                                        )
        self.module = Module.objects.create(title = 'test',
	                                                    user = self.user,
	                                                    hours = 3,	
                                                        )

    # metodo de test
    # prueba el registro
    # de un nuevo Page                                            
    def test_new_page(self):
        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/pages/newpage')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'Prueba',
                'content': 'hola',
                }

        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        new_page_module(req,self.course.id,self.module.id)
        page = Page.objects.get(title='Prueba')
        assert page
        return page
    
    # metodo de test
    # prueba eliminar
    # una Page 
    def test_delete_page(self):
        page=PageTest.test_new_page(self)
        page_id=page.id

        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/pages/{page_id}/delete')
        req.user = self.user
        delete_page(req,self.course.id,self.module.id,page_id)
        try:
            page = Course.objects.get(id = page_id)
            assert False
        except Exception:
            assert True

    # metodo de test
    # prueba detalles
    # de un nuevo page 
    def test_deta_page(self):
        page=PageTest.test_new_page(self)
        page_id=page.id
        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/pages/{page_id}')
        req.user = self.user
        page_detail(req,self.course.id,self.module.id,page_id)
        page01 = Page.objects.get(title='Prueba')
        assert page01
        return page01

    # metodo de test
    # prueba mmarcar page
    # de una page 
    def test_mark_page(self):
        page=PageTest.test_new_page(self)
        page_id=page.id    
        req = self.factory.get('')
        req.user = self.user
        mark_page_as_done(req,self.course.id,self.module.id,page_id)
        mod01=Module.objects.get(id=self.module.id)
        assert mod01
