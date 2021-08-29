from django.core.files import uploadedfile
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.forms.widgets import Media
from module.models import Module
from django.contrib.messages.storage.fallback import FallbackStorage
from classroom.models import Category, Course
from django.test import TestCase
from .models import Assignment, Submission
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import assignment_detail, delete_assignment, edit_assignment, new_assignment, new_submission
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# Create your tests here.

# clase de test
# contiene las funciones
# para probar los metodos
# de assignments
class AssTest(TestCase):
    # metodo setup
    # establece valores
    # iniciales que se utilizaran
    # en la suite de tests
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
        

    # metodo de test
    # prueba la creacion
    # de un nuevo assignment
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

        new_assignment(req,self.course.id,self.module.id)

        ass01 = Assignment.objects.get(title = 'test')
        assert ass01
        return ass01

    # metodo de test
    # prueba la edicion
    # de un assignment existente
    def test_edit_ass(self):
        ass = AssTest.test_new_ass(self)
        ass_id = ass.id
        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/assignment/{ass_id}/edit')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'test02',
	            'content': 'test02',
	            'points': 20,
	            'due': '11/08/2021',
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
       
        
        edit_assignment(req,self.course.id,self.module.id,ass_id)

        ass02 = Assignment.objects.get(title = 'test02')
        assert ass02

    # metodo de test
    # prueba la remocion
    # de un assignment existente
    def test_delete_ass(self):
        ass = AssTest.test_new_ass(self)
        ass_id = ass.id
        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/assignment/{ass_id}/delete')
        req.user = self.user
        delete_assignment(req,self.course.id,self.module.id,ass_id)
        try:
            ass=Assignment.objects.get(id=ass_id)
            assert False
        except Exception:
            assert True

    # metodo de test
    # prueba ver los detalles
    # de un assignment existente
    def test_ass_detail(self):
        ass = AssTest.test_new_ass(self)
        ass_id = ass.id
        req = self.factory.post(f'{self.course.id}/modules/{self.module.id}/assignment/{ass_id}')
        req.user = self.user
        assignment_detail(req,self.course.id,self.module.id,ass_id)
        ass04 = Assignment.objects.get(title='test')
        assert ass04


        





