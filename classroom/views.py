from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db.models import Q
from classroom.models import Course, Category, Grade

from classroom.forms import NewCourseForm, NewGradeForm

import json


# Create your views here.

@login_required
def index(request):
    user = request.user
    courses = Course.objects.filter(enrolled=user)
    for course in courses:
        print(course.id, course.title)

    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)


def Schedule(request):
    return render(request, 'classroom/schedule.html')


def Categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'classroom/categories.html', context)


def CategoryCourses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)

    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'classroom/categorycourses.html', context)


def NewCourse(request):
    user = request.user
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
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
            return redirect('my-courses')
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    return render(request, 'classroom/newcourse.html', context)


@login_required
def CourseDetail(request, course_id):
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


@login_required
def Enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.add(user)
    return redirect('index')


@login_required
def DeleteCourse(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    # if user != course.user:
    #	return HttpResponseForbidden()
    # else:
    course.delete()
    return redirect('my-courses')


@login_required
def EditCourse(request, course_id):
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
                return redirect('my-courses')
        else:
            form = NewCourseForm(instance=course)

    context = {
        'form': form,
        'course': course
    }

    return render(request, 'classroom/editcourse.html', context)


def MyCourses(request):
    user = request.user
    courses = Course.objects.filter(user=user)

    context = {
        'courses': courses
    }

    return render(request, 'classroom/mycourses.html', context)


def Submissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False
    if user == course.user:
        teacher_mode = True
    grades = Grade.objects.filter(course=course, submission__user=user)
    context = {
        'grades': grades,
        'course': course,
        'teacher_mode': teacher_mode
    }
    return render(request, 'classroom/submissions.html', context)


def StudentSubmissions(request, course_id):
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


def GradeSubmission(request, course_id, grade_id):
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


def StudentsNotas(request, course_id):
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


def StudentEnrollList(request, course_id):
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

def AddStundentEnroll( request , course_id, student_id):
    user = request.user
    student = get_object_or_404( User, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.add(student)
    return redirect('students', course_id=course_id)  

def DeleteStundentEnroll( request , course_id, student_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404( User, id=student_id)
    course.enrolled.remove(student)
    return redirect('students', course_id=course_id)   


def StudentGrades(request, course_id):
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
            grade = Grade.objects.get_or_create(course=course, student=student)
    
    grades = Grade.objects.filter(course=course)
    
    context = {
        'course': course,
        'students': students,
        'grades': grades,
        'form': form
    }
    return render(request, 'classroom/studentgrades.html', context)
