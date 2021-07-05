from django.urls import path
from classroom.views import Categories, CategoryCourses, NewCourse, Enroll, DeleteCourse, EditCourse, MyCourses, CourseDetail, Submissions, StudentSubmissions, GradeSubmission

from module.views import NewModule, CourseModules
from page.views import DeletePage, NewPageModule, PageDetail, DeletePage
from assignment.views import NewAssignment, AssignmentDetail, EditAssignment, DeleteAssignment

urlpatterns = [
	#Course - Classroom Views
	path('newcourse/', NewCourse, name='newcourse'),
	path('MyCourses/', MyCourses, name='my-courses'),
	path('categories/', Categories, name='categories'),
	path('categories/<category_slug>', CategoryCourses, name='category-courses'),
	path('<course_id>/', CourseDetail, name='course'),
	path('<course_id>/enroll', Enroll, name='enroll'),
	path('<course_id>/edit', EditCourse, name='edit-course'),
	path('<course_id>/delete', DeleteCourse, name='delete-course'),
	#Modules
	path('<course_id>/modules', CourseModules, name='modules'),
	path('<course_id>/modules/newmodule', NewModule, name='new-module'),
	#Pages
	path('<course_id>/modules/<module_id>/pages/newpage', NewPageModule, name='new-page'),
	path('<course_id>/modules/<module_id>/pages/<page_id>', PageDetail, name='page-detail'),
	path('<course_id>/modules/<module_id>/pages/<page_id>/delete', DeletePage, name='delete-page'),
	#Assignment
	path('<course_id>/modules/<module_id>/assignment/newassignment', NewAssignment, name='new-assignment'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>', AssignmentDetail, name='assignment-detail'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>/edit', EditAssignment, name='assignment-edit'),
	path('<course_id>/modules/<module_id>/assignment/<assignment_id>/delete', DeleteAssignment, name='assignment-delete'),
	#Submissions
	path('<course_id>/submissions', Submissions, name='submissions'),
	path('<course_id>/studentsubmissions', StudentSubmissions, name='student-submissions'),
	path('<course_id>/submissions/<grade_id>/grade', GradeSubmission, name='grade-submission'),

]