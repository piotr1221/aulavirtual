from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from assignment.forms import NewAssignmentForm, NewSubmissionForm
from assignment.models import AssignmentFileContent, Assignment, Submission

from module.models import Module
from classroom.models import Course

import datetime


# Create your views here.


# Esta función muestra la vista con el formulario para 
# crear una nueva tarea, además recibe, procesa y 
# crea una nueva tarea
def new_assignment(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objs = []

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                points = form.cleaned_data.get('points')
                due = form.cleaned_data.get('due')
                files = request.FILES.getlist('files')

                for file in files:
                    file_instance = AssignmentFileContent(file=file, user=user)
                    file_instance.save()
                    files_objs.append(file_instance)

                a = Assignment.objects.create(title=title, content=content, points=points, due=due)
                a.files.set(files_objs)
                a.save()
                initialize_submissions(course_id, a.id)
                module.assignments.add(a)
                return redirect('modules', course_id=course_id)
        else:
            form = NewAssignmentForm()

    context = {
        'form': form,
    }
    return render(request, 'assignment/newassignment.html', context)


# Esta función muestra la vista con el formulario para 
# editar una tarea, además recibe, procesa y 
# edita la nueva tarea
def edit_assignment(request, course_id, module_id, assignment_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    files_objs = []

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES, instance=assignment)
            if form.is_valid():
                assignment.title = form.cleaned_data.get('title')
                assignment.content = form.cleaned_data.get('content')
                assignment.points = form.cleaned_data.get('points')
                assignment.due = form.cleaned_data.get('due')
                files = request.FILES.getlist('files')

                for file in files:
                    file_instance = AssignmentFileContent(file=file, user=user)
                    file_instance.save()
                    files_objs.append(file_instance)

                assignment.files.set(files_objs)
                assignment.save()
                return redirect('modules', course_id=course_id)
        else:
            form = NewAssignmentForm(instance=assignment)
            form.files = assignment.files

    context = {
        'form': form,
        'course_id': course_id,
        'module_id': module_id,
        'assignment_id': assignment_id
    }
    return render(request, 'assignment/editassignment.html', context)

# Esta función elimina una tarea
def delete_assignment(request, course_id, module_id, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    return redirect('modules', course_id=course_id)

# Esta función muestra la vista que contiene 
# los detalles de una tarea
def assignment_detail(request, course_id, module_id, assignment_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    context = {
        'assignment': assignment,
        'course_id': course_id,
        'module_id': module_id,
        'teacher_mode': teacher_mode,
    }

    return render(request, 'assignment/assignment.html', context)


# Esta función crea respuestas de tarea
# para todos los alumnos del curso
def initialize_submissions(course_id, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = get_object_or_404(Course, id=course_id)
    
    for student in course.enrolled.all():
        Submission.objects.create(user=student, assignment=assignment, date=None)
    
    return redirect('modules', course_id=course_id)


# Esta función muestra el formulario para que
# el estudiante responda la tarea que se le asignó,
# además recibe la información, procesa y actualiza

def new_submission(request, course_id, module_id, assignment_id):
    student = request.user
    get_object_or_404(Course, id=course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    submission, c = Submission.objects.get_or_create(user=student, assignment_id=assignment_id)

    if request.method == 'POST':
        form = NewSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            file = request.FILES.get('file')
            submission.file = file
            submission.delivered = True
            submission.date = datetime.date.today()
            submission.save()

            request.session['status_message'] = "¡Tarea enviada exitosamente!"
            return redirect('modules', course_id=course_id)
    else:
        form = NewSubmissionForm(instance=submission)

    context = {
        'assignment': assignment, 
        'form': form
    }
    return render(request, 'assignment/submitassignment.html', context)


def student_submission(request, course_id, module_id, assignment_id, submission_id):
    assignment = Assignment.objects.get(id=assignment_id)
    submission = get_object_or_404(Submission, id=submission_id)     
    
    if request.method == 'POST':
        submission_point = request.POST.get('points') 
        submission.points = submission_point
        submission.checked = True
        submission.save()
        messages.success(request, "La nota se ha asignado exitosamente")

    context = {
        'assignment': assignment,
        'submission': submission,
        'course_id': course_id
    }
    try:
        context['submission_file'] =  submission.file.url
    except:
        pass

    return render(request, 'assignment/studentsubmission.html', context)