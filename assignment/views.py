from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from assignment.forms import NewAssignmentForm, NewSubmissionForm
from assignment.models import AssignmentFileContent, Assignment, Submission

from module.models import Module
from classroom.models import Course, Grade
from completion.models import Completion

import datetime


# Create your views here.
def NewAssignment(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objs = []

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES)
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
                InitializeSubmissions(course_id, a.id)
                module.assignments.add(a)
                return redirect('modules', course_id=course_id)
        else:
            form = NewAssignmentForm()

    context = {
        'form': form,
    }
    return render(request, 'assignment/newassignment.html', context)


def EditAssignment(request, course_id, module_id, assignment_id):
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

def DeleteAssignment(request, course_id, module_id, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    return redirect('modules', course_id=course_id)

def AssignmentDetail(request, course_id, module_id, assignment_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    assignment = get_object_or_404(Assignment, id=assignment_id)
    my_submissions = Submission.objects.filter(assignment=assignment, user=user)

    context = {
        'assignment': assignment,
        'course_id': course_id,
        'my_submissions': my_submissions,
        'module_id': module_id,
        'teacher_mode': teacher_mode,
    }
    return render(request, 'assignment/assignment.html', context)


def InitializeSubmissions(course_id, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = get_object_or_404(Course, id=course_id)
    
    for student in course.enrolled.all():
        submission = Submission.objects.create(user=student, assignment=assignment, date=None)
    
    return redirect('modules', course_id=course_id)


def NewSubmission(request, course_id, module_id, assignment_id):
    student = request.user
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = Submission.objects.get(user=student, assignment_id=assignment_id)

    if request.method == 'POST':
        form = NewSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            file = request.FILES.get('file')
            submission.file = file
            submission.delivered = True
            submission.date = datetime.date.today()
            submission.save()
            return redirect('modules', course_id=course_id)
    else:
        form = NewSubmissionForm(instance=submission)

    context = {
        'form': form,
        'assignment': assignment
    }
    return render(request, 'assignment/submitassignment.html', context)
