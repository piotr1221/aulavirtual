from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from module.forms import NewModuleForm
from module.models import Module
from classroom.models import Course

from completion.models import Completion


# Create your views here.
#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def new_module(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewModuleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                hours = form.cleaned_data.get('hours')
                m = Module.objects.create(title=title, hours=hours, user=user)
                course.modules.add(m)
                course.save()
                return redirect('modules', course_id=course_id)
        else:
            form = NewModuleForm()

    context = {
        'form': form,
    }

    return render(request, 'module/newmodule.html', context)

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def delete_module(request, course_id, module_id):
    module = get_object_or_404(Module, id=module_id)
    module.delete()
    return redirect('modules', course_id=course_id)

#Funcion Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
#Texto Prueba
def course_modules(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    page_completions = Completion.objects.filter(user=user, course=course).values_list('page__pk', flat=True)
    quiz_completions = Completion.objects.filter(user=user, course=course).values_list('quiz__pk', flat=True)
    assignment_completions = Completion.objects.filter(user=user, course=course).values_list('assignment__pk',
                                                                                             flat=True)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    if ('status_message' in request.session):
        message = request.session['status_message']
        del request.session['status_message']
        messages.success(request, message)

    context = {
        'teacher_mode': teacher_mode,
        'course': course,
        'page_completions': page_completions,
        'quiz_completions': quiz_completions,
        'assignment_completions': assignment_completions,
    }

    return render(request, 'module/modules.html', context)
