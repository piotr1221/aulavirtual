from django.test import TestCase
from .models import Category, Course, Grade
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import add_stundent_enroll, delete_course, new_course,edit_course, enroll, delete_course, grade_submission,delete_stundent_enroll, student_grades
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

        self.course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocrona',
                                            day='LU',
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

    def test_edit_course(self):
        req = self.factory.post(f'course/{self.course.id}/edit')
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

        edit_course(req,self.course.id)
        course = Course.objects.get(title = 'Español')
        assert course

    def test_enroll(self):
        req = self.factory.post(f'course/{self.course.id}/enroll')
        req.user = self.user
        enroll(req,self.course.id)

        for user_enrolled in self.course.enrolled.all():
            if user_enrolled.id == self.user.id:
                assert True
            else:
                assert False

    def test_delete_course(self):

        course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocronakbro',
                                            day='JU',
                                            time_start='10:00',
                                            time_end='11:00',
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )

        req = self.factory.post(f'course/{course.id}/delete')
        req.user = self.user
        delete_course(req,course.id)
        try:
            course = Course.objects.get(id = course.id)
            assert False
        except Exception:
            assert True

    def test_add_student_enroll(self):
        
        req = self.factory.post(f'{self.course.id}/students/{self.student.id}/add')
        req.user = self.user

        add_stundent_enroll(req,self.course.id,self.student.id)

        for user_enrolled in self.course.enrolled.all():
            if user_enrolled.id == self.student.id:
                assert True
            else:
                assert False

    def test_delete_student_enroll(self):
        course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocrona',
                                            day='VI',
                                            time_start='08:00',
                                            time_end='11:00',
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )

        course.enrolled.add(self.student)

        student = User.objects.create_user(username='test',
                                            email='test@testing.com',
                                            password='testingfunction',
                                            )

        req = self.factory.post(f'{course.id}/students/{student.id}/delete')
        req.user = self.user

        delete_stundent_enroll(req,course.id,student.id)

        for user_enrolled in course.enrolled.all():
            if user_enrolled.id == student.id:
                assert False
            else:
                assert True

    def test_grade_submission(self):
        req = self.factory.post(f'{self.course}/submissions/{self.grade}/grade')
        req.user = self.user
        grade_submission(req,self.course.id, self.grade.id)
        grade = Grade.objects.get(id = self.grade.id)
        assert grade
    
    def test_student_grades(self):
        req = self.factory.post(f'{self.course}/students/grades')
        req.user = self.user
        student_grades(req,self.course.id)
        grades = Grade.objects.filter(course = self.course)
        assert grades

    

    
        

