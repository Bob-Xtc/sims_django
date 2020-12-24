from django.urls import path
# sims路由

from sims.views import student_login, student_register, student_choose_course, teacher_create_course, student_deregister


urlpatterns = [
    path('student/login/', student_login, name='studentLogin'),
    path('student/register/', student_register, name='studentRegister'),
    path('chooseCourse/', student_choose_course, name='chooseCourse'),
    path('createCourse/', teacher_create_course, name='createCourse'),
    path('accountDelete/', student_deregister, name='accountDelete'),
]
