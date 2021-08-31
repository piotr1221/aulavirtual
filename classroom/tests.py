from module.models import Module
from assignment.models import Assignment, AssignmentFileContent, Submission
from django.test import TestCase
from .models import Category, Course, Grade
from datetime import datetime
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from .views import add_stundent_enroll, categories, category_courses, course_detail, delete_course, get_student_courses, index, initialize_arrays, my_courses, new_course,edit_course, enroll, delete_course, grade_submission,delete_stundent_enroll, rate_submissions, schedule, sort_times, student_enroll_list, student_grades, student_submissions, students_notas, submissions, verify_schedule, verify_time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
import datetime

# Create your tests here.

# clase de test
# contiene las funciones
# para probar los metodos
# de classroom
class CourseTest(TestCase):
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
                                            time_start=datetime.datetime.strptime('01:00', '%H:%M').time(),
                                            time_end=datetime.datetime.strptime('02:00', '%H:%M').time(),
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
        self.course.enrolled.add(self.student)
    # metodo de testf
    # prueba el registro
    # de un nuevo curso                                            
    def test_new_course(self):
        req = self.factory.post('course/newcourse')
        req.user = self.user

        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'English',
                'category': self.category.id,
                'day': '1',
                'description': 'Basic Intermediate Advance English course',
                'time_start': datetime.datetime.strptime('03:00', '%H:%M').time(),
                'time_end': datetime.datetime.strptime('04:00', '%H:%M').time(),
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

    # # metodo de test
    # # prueba el editar
    # # de un nuevo curso
    def test_edit_course(self):
        req = self.factory.post(f'course/{self.course.id}/edit')
        req.user = self.user
        info = {'csrfmiddlewaretoken': get_token(req),
                'title': 'Español',
                'category': self.category.id,
                'day': '4',
                'description': 'Curso basico, intermedio, avanzado de Español',
                'time_start': datetime.datetime.strptime('05:00', '%H:%M').time(),
                'time_end': datetime.datetime.strptime('06:00', '%H:%M').time(),
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

    # # metodo de test
    # # prueba registrarse
    # # de un nuevo curso 
    def test_enroll(self):
        req = self.factory.post(f'course/{self.course.id}/enroll')
        req.user = self.student

        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        enroll(req,self.course.id)
        
        for user_enrolled in self.course.enrolled.all():
            print(user_enrolled.id, self.student.id)
            if user_enrolled.id == self.student.id:
                assert True
                return
        assert False

    # # metodo de test
    # # prueba la remocion
    # # de un nuevo curso 
    def test_delete_course(self):

        course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocronakbro',
                                            day='4',
                                            time_start=datetime.datetime.strptime('07:00', '%H:%M').time(),
                                            time_end=datetime.datetime.strptime('08:00', '%H:%M').time(),
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

    # # metodo de test
    # # prueba la agregacion
    # # de un nuevo estudiante 
    def test_add_student_enroll(self):
        
        req = self.factory.post(f'course/{self.course.id}/students/{self.student.id}/add')
        req.user = self.user

        add_stundent_enroll(req,self.course.id,self.student.id)

        for user_enrolled in self.course.enrolled.all():
            if user_enrolled.id == self.student.id:
                assert True
            else:
                assert False

    # # metodo de test
    # # prueba la remocion
    # # de un nuevo alumno 
    def test_delete_student_enroll(self):
        course = Course.objects.create(picture=None,
                                            title='test_course',
                                            description='xocrona',
                                            day='5',
                                            time_start=datetime.datetime.strptime('09:00', '%H:%M').time(),
                                            time_end=datetime.datetime.strptime('10:00', '%H:%M').time(),
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )

        course.enrolled.add(self.student)

        student = User.objects.create_user(username='test',
                                            email='test@testing.com',
                                            password='testingfunction',
                                            )

        req = self.factory.post(f'course/{course.id}/students/{student.id}/delete')
        req.user = self.user

        delete_stundent_enroll(req,course.id,student.id)

        for user_enrolled in course.enrolled.all():
            if user_enrolled.id == student.id:
                assert False
            else:
                assert True

    # # metodo de test
    # # prueba el registro
    # # de notas de tareas 
    def test_grade_submission(self):
        req = self.factory.post(f'course/{self.course}/submissions/{self.grade}/grade')
        req.user = self.user
        grade_submission(req,self.course.id, self.grade.id)
        grade = Grade.objects.get(id = self.grade.id)
        assert grade
    
    # # metodo de test
    # # prueba el registro
    # # de un nuevo curso 
    def test_student_grades(self):
        req = self.factory.post(f'course/{self.course}/students/grades')
        req.user = self.user
        student_grades(req,self.course.id)
        grades = Grade.objects.filter(course = self.course)
        assert grades

    # # metodo de test
    # # prueba la visualizacion
    # # del horario de cursos
    def test_schedule(self):
        req = self.factory.get('course/schedule')
        req.user = self.user
        schedule(req)

    # # metodo de test
    # # prueba la visualizacion
    # # de las categorias
    def test_categories(self):
        req = self.factory.get('course/categories')
        req.user = self.user
        categories(req)

    # # metodo de test
    # # prueba la visualizacion
    # # de cursos de una categoria
    def test_category_courses(self):
        req = self.factory.get(f'course/categories/{self.category.slug}')
        req.user = self.user
        category_courses(req, self.category.slug)

    # # metodo de test
    # # prueba la visualizacion
    # # de los detalles de curso
    def test_course_detail(self):
        req = self.factory.get(f'course/{self.course.id}')
        req.user = self.user
        course_detail(req, self.course.id)

    # # metodo de test
    # # prueba la visualizacion
    # # del horario de cursos
    def test_my_courses(self):
        req = self.factory.get('course/mycourses')
        req.user = self.user
        my_courses(req)

    # # metodo de test
    # # prueba la entrega
    # # de tareas
    def test_submissions(self):
        req = self.factory.get(f'course/{self.course.id}/submissions')
        req.user = self.user
        submissions(req, self.course.id)
    
    # # metodo de test
    # # prueba la entrega
    # # de tareas de alumno
    def test_student_submissions(self):
        req = self.factory.get(f'course/{self.course.id}/studentsubmissions')
        req.user = self.user
        student_submissions(req, self.course.id)

    # # metodo de test
    # # prueba la agregacion
    # # de alumno a curso
    def test_student_enroll_list(self):
        req = self.factory.get(f'course/{self.course.id}/students')
        req.user = self.user
        student_enroll_list(req, self.course.id)

    # # metodo de test
    # # prueba la entrega
    # # de tareas
    def test_index(self):
        req = self.factory.get('')
        req.user = self.user
        index(req)

    # # metodo de test
    # # prueba la agregacion
    # # de alumno a curso
    def test_init_array(self):
        courses = get_student_courses(self.user)
        u_courses = []
        times = []
        req = self.factory.get('')
        req.user = self.user
        initialize_arrays(courses,u_courses,times)

    # metodo de test
    # prueba la agregacion
    # de alumno a curso
    def test_sort(self):
        course04 = Course.objects.create(picture=None,
                                            title='test_course04',
                                            description='xocronakbro',
                                            day='2',
                                            time_start= datetime.datetime.strptime('11:00', '%H:%M').time(),
                                            time_end= datetime.datetime.strptime('12:00', '%H:%M').time(),
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )

        times = []
        times.append(course04.time_start)
        times.append(self.course.time_start)
        req = self.factory.get('')
        req.user = self.user
        sort_times(times)

    # metodo de test
    # prueba la agregacion
    # de alumno a curso
    def test_verify_time(self):
        course03 = Course.objects.create(picture=None,
                                            title='test_course03',
                                            description='xocronakbro',
                                            day='2',
                                            time_start= datetime.time(14, 0),
                                            time_end= datetime.time(15, 0),
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )
        req = self.factory.get('')
        req.user = self.user
        verify_time(course03.time_start,course03.time_end,req)

    # metodo de test
    # prueba la agregacion
    # de alumno a curso
    def test_verify_schedule(self):
        course04 = Course.objects.create(picture=None,
                                            title='test_course03',
                                            description='xocronakbro',
                                            day='2',
                                            time_start= datetime.datetime.strptime('13:00', '%H:%M').time(),
                                            time_end= datetime.datetime.strptime('14:00', '%H:%M').time(),
                                            category=self.category,
                                            syllabus='Syllabus',
                                            user=self.user,
                                            )
        course04.enrolled.add(self.student)
        req = self.factory.get('')
        req.user = self.user
        verify_schedule(self.student,course04)

    # metodo de test
    # prueba la agregacion
    # de alumno a curso
    def test_rate_submission(self):
        req = self.factory.get(f'{self.course.id}/submissions/rate')
        req.user = self.user
        info = {'csrfmiddlewaretoken': get_token(req),
                'points':15
                }
        
        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

        q = QueryDict('', mutable=True)
        q.update(info)
        req.POST = q

        rate_submissions(req,self.course.id)
        course = Grade.objects.get(id = self.grade.id)
        assert course

    # metodo de test
    # prueba la agregacion
    # de alumno a curso
    def test_cargar_categorias_vacio(self):
        req = self.factory.get('')
        req.user = self.user
        Category.objects.all().delete()
        index(req)
