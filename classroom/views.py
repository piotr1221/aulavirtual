from assignment.models import Assignment, Submission
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from classroom.models import Course, Category, Grade

from classroom.forms import NewCourseForm, NewGradeForm

# CONSTANTES
MIS_CURSOS_URL = 'classroom/mycourses.html'
CURSOS_POR_CATEGORIA = 'classroom/categorycourses.html'

# Create your views here.

# Esta vista es el portal 
# donde el usuario
# puede visualizar los cursos 
# en que se ha inscrito
@login_required
def index(request):
    cargar_categorias()
    user = request.user
    courses = Course.objects.filter(enrolled=user)
    for course in courses:
        print(course.id, course.title)

    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)


# Esta vista muestra el horario 
# del alumno con todos los 
# cursos en que se ha matriculado
# organizados en base a la hora de inicio
def schedule(request):
    user = request.user
    courses = get_student_courses(user)
    u_courses = []
    times = []

    initialize_arrays(courses, u_courses, times)
    append_courses_schedule(courses, u_courses, times)

    context = {
        'courses': u_courses,
    }
    return render(request, 'classroom/schedule.html', context)

# Esta función inicializa los arreglos 
# usados en la función "schedule"
def initialize_arrays(courses, u_courses, times):
    for course in courses:
        time = course.time_start
        if time not in times:
            times.append(time)
            u_courses.append([])
    for u_course in u_courses:
        for _ in range(7):
            u_course.append(None)
    sort_times(times)
    print(times)

# Esta función organiza el arreglo
#  de horas de inicio de 
# los cursos del alumno usado en 
# la función "initialize_arrays" 
# usando el método de burbuja mejorada 
def sort_times(times):
    flag = False
    for i in range(0, len(times) - 1):
        if flag:
            break
        flag = True
        for j in range(0, len(times) - (i + 1)):
            if times[j] > times[j+1]:
                flag = False
                times[j], times[j+1] = times[j+1], times[j]
        
# Este método organiza el arreglo 
# de cursos del alumno
# usado en la función "schedule" 
# según el arreglo de 
# horas de inicio de esa misma función y el día
def append_courses_schedule(courses, u_courses, times):
    for course in courses:
        for i in range(0, len(times)):
            if course.time_start == times[i]:
                u_courses[i][int(course.day)-1] = course
                break
 
# Esta función muestra la vista con las 
# categorías de todos los cursos que hay
def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'classroom/categories.html', context)

# Esta función muestra 
# la vista con los cursos
# que se encuentran en una 
# categoría seleccionada
def category_courses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)

    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, CURSOS_POR_CATEGORIA, context)

# Esta función muestra la vista
# con el formulario para un
# nuevo curso y también lo recupera,
# procesa, y crea el curso
def new_course(request):
    user = request.user
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            time_start = form.cleaned_data.get('time_start')
            time_end = form.cleaned_data.get('time_end')
            if verify_time(time_start, time_end, request):
                picture = form.cleaned_data.get('picture')
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                time_start = form.cleaned_data.get('time_start')
                time_end = form.cleaned_data.get('time_end')
                category = form.cleaned_data.get('category')
                syllabus = form.cleaned_data.get('syllabus')
                Course.objects.create(picture=picture, title=title, description=description, 
                time_start=time_start, time_end=time_end, category=category,
                syllabus=syllabus, user=user)
                
                courses = Course.objects.filter(user=user)
                messages.success(request, '¡El curso ha sido creado con éxito!')
                return render(request, MIS_CURSOS_URL, {'courses': courses})
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    return render(request, 'classroom/newcourse.html', context)

# Esta función verifica las 
# condiciones que deben de 
# cumplir la hora de inicio y 
# fin de la función "new_course"
def verify_time(time_start, time_end, request):
    result = True
    if time_start > time_end:
        result = False
        messages.error(request, 'La hora de inicio no puede ser mayor a la de fin.')
    if (time_start.minute > 0) or (time_end.minute > 0):
        result = False
        messages.error(request, 'Los cursos deben de iniciar y acabar en una hora en punto.')
    return result

# Esta función muestra la 
# vista que contiene 
# todos los detalles de un curso
@login_required
def course_detail(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False

    if user == course.user:
        teacher_mode = True

    context = {
        'course': course,
        'teacher_mode': teacher_mode,
    }

    return render(request, 'classroom/course.html', context)

# Esta función permite a un 
# usuario inscribirse a un curso
@login_required
def enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if verify_schedule(user, course):
        course.enrolled.add(user)
        return redirect('index')
    else:
        category = get_object_or_404(Category, id=course.category_id)
        context = {
            'category': category,
            'courses': Course.objects.all()
        }
        messages.error(request, 'No puedes matricularte porque tienes un curso que se cruza con este')
        return render(request, CURSOS_POR_CATEGORIA, context)


# Esta función devuelve los
#  cursos en los que un
# usuario se encuenta inscrito
def get_student_courses(user):
    courses = []
    for course in Course.objects.all():
        students = course.enrolled.all()
        if students.filter(id=user.id).exists():
            courses.append(course)
    return courses


# Esta función comprueba si
# el horario de un curso
# se cruza con algún curso 
# en el que ya esté inscrito
# un usuario
def verify_schedule(user, new_course):
    courses = get_student_courses(user)
    for course in courses:
        nts, nte = new_course.time_start, new_course.time_end
        cts, cte = course.time_start, course.time_end
        # La hora de inicio y fin del 
        # nuevo curso deben de darse
        # ambos antes del inicio de un 
        # curso o después de su fin
        c1 = (nts <= cts and nte <= cts)
        c2 = (cte <= nts and cte <= nte)
        c3 = course.day == new_course.day 
        print(c1)
        print(c2)
        print(c3)
        if not(c1 or c2) and c3:
            return False
    return True


# Esta función elimina un curso
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('my-courses')


# Esta función muestra la vista
#  que contiene el formulario
# para editar la información de
#  un curso, además recupera
# la información ingresa, la 
# procesa y edita el curso
@login_required
def edit_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()

    else:
        if request.method == 'POST':
            form = NewCourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                course.picture = form.cleaned_data.get('picture')
                course.title = form.cleaned_data.get('title')
                course.description = form.cleaned_data.get('description')
                course.day = form.cleaned_data.get('day')
                course.time_start = form.cleaned_data.get('time_start')
                course.time_end = form.cleaned_data.get('time_end')
                course.category = form.cleaned_data.get('category')
                course.syllabus = form.cleaned_data.get('syllabus')
                course.save()

                courses = Course.objects.filter(user=user)
                messages.success(request, '¡El curso ha sido editado con éxito!')
                return render(request, MIS_CURSOS_URL, {'courses': courses})
        else:
            form = NewCourseForm(instance=course)

    context = {
        'form': form,
        'course': course
    }

    return render(request, 'classroom/editcourse.html', context)

# Esta función muestra la 
# vista que contiene
# los cursos creados por 
# el usuario activo
def my_courses(request):
    user = request.user
    courses = Course.objects.filter(user=user)

    context = {
        'courses': courses
    }

    return render(request, MIS_CURSOS_URL, context)

# Esta función muestra la 
# vista de las tareas
# que ha entregado el
#  alumno por módulo
def submissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    submissions = Submission.objects.filter(user=user)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True
    
    context = {
        'course': course,
        'teacher_mode': teacher_mode,
        'submissions': submissions
    }
    return render(request, 'classroom/submissions.html', context)

# *Esta función muestra 
# al estudiante sus 
# tareas entregadas y 
# las notas de estas
def student_submissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    
    if user != course.user:
        return HttpResponseForbidden()
    else:
        grades = Grade.objects.filter(course=course)
        context = {
            'course': course,
            'grades': grades,
        }
    return render(request, 'classroom/studentgrades.html', context)

# Esta función muestra al 
# profesor las tareas entregadas
# por un estudiante y un 
# formulario para modificar sus notas

def rate_submissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    students = course.enrolled.all()
    students_id = []
    for student in students:
        students_id.append(student.id)         

    if request.method == 'POST':
        submission_point = request.POST.getlist('points') 
        submission_id = request.POST.getlist('submission_id')
        message = ""
        for i in range(len(submission_point)):
            submission = Submission.objects.get(id=submission_id[i])
            submission.points = submission_point[i]
            submission.checked = True
            submission.save()
            message = "Las notas se ha asignado exitosamente"
        messages.success(request, message)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    submissions = Submission.objects.filter(user_id__in=students_id)  
    
    context = {
        'course': course,
        'teacher_mode': teacher_mode,
        'submissions': submissions,
    }
    return render(request, 'classroom/ratesubmissions.html', context)


# La hora de inicio y fin del 
# nuevo curso deben de darse
# ambos antes del inicio de un 
# curso o después de su fin
def grade_submission(request, course_id, grade_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grade = get_object_or_404(Grade, id=grade_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            points = request.POST.get('points')
            grade.points = points
            grade.status = 'graded'
            grade.graded_by = user
            grade.save()
            return redirect('student-submissions', course_id=course_id)
    context = {
        'course': course,
        'grade': grade,
    }

    return render(request, 'classroom/gradesubmission.html', context)

# *Esta función muestra 
# las notas de un estudiante
# de forma general en un curso
def students_notas(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if user != course.user:
        return HttpResponseForbidden()
    else:
        #retorna lista de tareas por curso
        assignments = Assignment.objects.filter( user = user )
        #retorna lista de alumnos por curso
        students = User.objects.filter( course = course )
        
        grades = Grade.objects.filter( course = course)
        

        context = {
            'course': course,
            'assignments': assignments,
            'students' : students,
            'grades': grades,
        }
    return render(request, 'classroom/editnotas.html', context)

# Esta función muestra una
# vista con la lista de
# estudiantes por curso además
# de opciones de agregar y eliminar
def student_enroll_list(request, course_id):
    busqueda = request.POST.get("buscar")
    user = request.user
    students = User.objects.all()
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False
    if user == course.user:
        teacher_mode = True
    if busqueda:
        students = User.objects.filter(
            Q(email=busqueda)
        ).distinct()
    context = {
        'teacher_mode': teacher_mode,
        'course': course,  
        'students' :students    
    }
    return render(request, 'classroom/studentsenroll.html', context)



# Esta función añade estudiantes
# a la lista de matriculados en un curso
def add_stundent_enroll( request , course_id, student_id):
    student = get_object_or_404( User, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.add(student)
    return redirect('students', course_id=course_id)  


# Esta función elimina estudiantes
# de la lista de matriculados en un curso
def delete_stundent_enroll( request , course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404( User, id=student_id)
    course.enrolled.remove(student)
    if request.user != student: 
        return redirect('students', course_id=course_id)   
    else:
        return redirect('index')


# Esta función muestra las
# notas de los alumnos
# en general de todo el curso
def student_grades(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    students = course.enrolled.all()

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    if request.method == 'POST':
        grades_grade = request.POST.getlist('grade') 
        students_id = request.POST.getlist('student_id')
        for i in range(len(students_id)):
            grade = Grade.objects.get(course=course, student_id=students_id[i])
            grade.grade = grades_grade[i]
            grade.save()
            print("Confirmado")
        return redirect('modules', course_id=course_id)
    else:
        form = NewGradeForm()
        for student in students:
            Grade.objects.get_or_create(course=course, student=student)
    
    grades = Grade.objects.filter(course=course)
    
    context = {
        'course': course,
        'students': students,
        'grades': grades,
        'form': form,
         'teacher_mode': teacher_mode,
    }
    return render(request, 'classroom/studentgrades.html', context)

# Esta función genera categorías
# para los cursos en caso de no existir
def cargar_categorias():
	if not Category.objects.all():
		Category.objects.create(title='Ciencia', icon='ciencia', slug='ciencia')
		Category.objects.create(title='Humanidades', icon='humanidades', slug='humanidades')
		Category.objects.create(title='Música', icon='música', slug='música')