from django.urls import path
from classroom.views import categories, category_courses, new_course, enroll, delete_course, edit_course
from classroom.views import my_courses, course_detail, schedule, student_grades, submissions, student_submissions, grade_submission, students_notas, student_enroll_list,delete_stundent_enroll,add_stundent_enroll

from module.views import new_module, course_modules
from page.views import delete_page, new_page_module, page_detail, delete_page
from assignment.views import new_assignment, assignment_detail, edit_assignment, delete_assignment, new_submission

urlpatterns = [
	#Course - Classroom Views
	path('newcourse/', new_course, name='newcourse'),
	path('mycourses/', my_courses, name='my-courses'),
	path('schedule/', schedule, name='schedule'),
	path('categories/', categories, name='categories'),
	path('categories/<category_slug>', category_courses, name='category-courses'),
	path('<course_id>/', course_detail, name='course'),
	path('<course_id>/enroll', enroll, name='enroll'),
	path('<course_id>/edit', edit_course, name='edit-course'),
	path('<course_id>/delete', delete_course, name='delete-course'),
 	path('<course_id>/student_notas', students_notas, name='student-notas'),
	#Modules
	path('<course_id>/modules', course_modules, name='modules'),
	path('<course_id>/modules/newmodule', new_module, name='new-module'),
	#Pages
	path('<course_id>/modules/<module_id>/pages/newpage', new_page_module, name='new-page'),
	path('<course_id>/modules/<module_id>/pages/<page_id>', page_detail, name='page-detail'),
	path('<course_id>/modules/<module_id>/pages/<page_id>/delete', delete_page, name='delete-page'),
	#Assignment
	path('<course_id>/modules/<module_id>/assignment/newassignment', new_assignment, name='new-assignment'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>', assignment_detail, name='assignment-detail'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>/edit', edit_assignment, name='assignment-edit'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>/delete', delete_assignment, name='assignment-delete'),
	#Submissions
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>/start', new_submission, name='start-assignment'),
	path('<course_id>/submissions', submissions, name='submissions'),
	path('<course_id>/studentsubmissions', student_submissions, name='student-submissions'),
	path('<course_id>/submissions/<grade_id>/grade', grade_submission, name='grade-submission'),
	#Students
	path('<course_id>/students', student_enroll_list, name='students'),
	path('<course_id>/students/grades', student_grades, name='students-grades'),
	path('<course_id>/students/<student_id>/delete', delete_stundent_enroll, name='delete-student'),
	path('<course_id>/students/<student_id>/add', add_stundent_enroll, name='add-student'),
]