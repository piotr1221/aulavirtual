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

# Esta vista es el portal donde el usuario
# puede visualizar los cursos en que se ha inscrito
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


# Esta vista muestra el horario del alumno con
# todos los cursos en que se ha matriculado
# organizados en base a la hora de inicio
def schedule(request):
    user = request.user
    courses = get_student_courses(user)
    u_courses = []
    times = []

    initialize_arrays(courses, u_courses, times)
    append_courses_schedule(courses, u_courses, times)
    fill_array(u_courses, times)

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
    sort_times(times)
    print(times)

# Esta función organiza el arreglo de horas de inicio 
# de los cursos del alumno usado en la función "schedule"
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
        
# Este método organiza el arreglo de cursos del alumno
# usado en la función "schedule" según el arreglo de 
# horas de inicio de esa misma función
def append_courses_schedule(courses, u_courses, times):
    for course in courses:
        for i in range(0, len(times)):
            if course.time_start == times[i]:
                u_courses[i].append(course)
                break

# Este método llena el arreglo de 
def fill_array(u_courses, times):
    for i in range(0, len(times)):
        u_courses[i].sort(key=lambda c: int(c.day))
        j = 0
        while j < 7:
            try:
                if int(u_courses[i][j].day) != (j + 1):
                    u_courses[i].insert(j, None)
            except Exception:
                u_courses[i].append(None)
            j += 1
 
#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'classroom/categories.html', context)

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def category_courses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)

    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, CURSOS_POR_CATEGORIA, context)

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def verify_time(time_start, time_end, request):
    result = True
    if time_start > time_end:
        result = False
        messages.error(request, 'La hora de inicio no puede ser mayor a la de fin.')
    if (time_start.minute > 0) or (time_end.minute > 0):
        result = False
        messages.error(request, 'Los cursos deben de iniciar y acabar en una hora en punto.')
    return result

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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


#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def get_student_courses(user):
    courses = []
    for course in Course.objects.all():
        students = course.enrolled.all()
        if students.filter(id=user.id).exists():
            courses.append(course)
    return courses

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def verify_schedule(user, new_course):
    courses = get_student_courses(user)
    for course in courses:
        nts, nte = new_course.time_start, new_course.time_end
        cts, cte = course.time_start, course.time_end
        # La hora de inicio y fin del nuevo curso deben de darse
        # ambos antes del inicio de un curso o después de su fin
        c1 = (nts <= cts and nte <= cts)
        c2 = (cte <= nts and cte <= nte)
        c3 = course.day == new_course.day 
        print(c1)
        print(c2)
        print(c3)
        if not(c1 or c2) and c3:
            return False
    return True

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # if user != course.user:
    #	return HttpResponseForbidden()
    # else:
    course.delete()
    return redirect('my-courses')

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def my_courses(request):
    user = request.user
    courses = Course.objects.filter(user=user)

    context = {
        'courses': courses
    }

    return render(request, MIS_CURSOS_URL, context)

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
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

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def add_stundent_enroll( request , course_id, student_id):
    student = get_object_or_404( User, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.add(student)
    return redirect('students', course_id=course_id)  

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def delete_stundent_enroll( request , course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404( User, id=student_id)
    course.enrolled.remove(student)
    if request.user != student: 
        return redirect('students', course_id=course_id)   
    else:
        return redirect('index')

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def student_grades(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.enrolled.all()

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
        'form': form
    }
    return render(request, 'classroom/studentgrades.html', context)

def cargar_categorias():
	if not Category.objects.all():
		Category.objects.create(title='Ciencia', icon='ciencia', slug='ciencia')
		Category.objects.create(title='Humanidades', icon='humanidades', slug='humanidades')
		Category.objects.create(title='Música', icon='música', slug='música')