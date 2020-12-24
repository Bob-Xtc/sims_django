import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.forms.models import model_to_dict

from sims.models import Student, Course, Course_2_Student, Teachers

# Create your views here.


def student_register(request):
    # 学生注册
    student_id = request.POST.get('student_id')
    password = request.POST.get('password')
    name = request.POST.get('name')
    birthday = request.POST.get('birthday')
    sex = request.POST.get('sex')
    major = request.POST.get('major')

    Student.objects.create(student_id=student_id, password=password,
                           name=name, birthday=birthday, sex=sex, 
                           major=major)

    resp = {
        'status' : 200,
        'message': '注册成功',
        'data': ''
    }
    return JsonResponse(resp)



def student_login(request):
    # 学生登录
    data = None
    status = 400
    message = None
    student_id = request.POST.get('student_id')
    password = request.POST.get('password')

    try:
      current_stu = Student.objects.get(student_id=student_id)
    except Exception:
      current_stu = None

    if not current_stu:
        message = "用户名不存在"
    elif current_stu.password != str(password):
        message = "密码不正确"
    else:
        if current_stu.is_delete:
            message = "该用户已注销"
        else:
            status = 200
            message = "登录成功"
            data = model_to_dict(current_stu)
            del data['password']

    resp = {
        'status' : status,
        'message': message,
        'data': data
    }
    
    return JsonResponse(resp, content_type="application/json")


def student_choose_course(request):
    # 学生选课
    course_name = request.POST.get('course_name')
    uuid = request.COOKIES.get('uuid')

    chosen_course = None
    status = 400
    message = None
    data = None

    try:
        current_stu = Student.objects.get(uuid=uuid)
        stu_major = current_stu.major
        chosen_course = Course.objects.get(name=course_name,
                                           major=stu_major)
    except Exception:
        if not chosen_course:
            message = "不存在此课程！"
    if chosen_course:
        if Course_2_Student.objects.filter(student=current_stu, course=chosen_course):
            message = "此课程已选择！"
        else:
            course_student_obj = Course_2_Student.objects.create(student=current_stu,
                                                                course=chosen_course)
            status = 200
            message = "选课成功！"
            data = model_to_dict(course_student_obj)
    
    resp = {
        'status' : status,
        'message': message,
        'data': data
    }

    return JsonResponse(resp, content_type="application/json")


def teacher_create_course(request):
    uuid = request.COOKIES.get('uuid')
    course_name = request.POST.get('course_name')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')

    teacher = None
    status = 400

    try:
        teacher = Teachers.objects.get(uuid=uuid)
    except:
        message = '非教师用户，无法进行此操作！'
    
    if teacher:
        Course.objects.create(name=course_name, major=teacher.major,
                              teacher=teacher)
        status = 200
        message = "课程创建成功！"
    
    resp = {
      'status': status,
      'message': message,
    }
    
    return JsonResponse(resp, content_type="application/json")


  
def student_deregister(request):
    uuid = request.POST.get('uuid')

    status = 400
    message = None
    current_stu = None

    try:
        current_stu = Student.objects.get(uuid=uuid)
    except Exception:
        message = "此账户不存在！"
    
    if current_stu:
        if current_stu.is_delete:
            message = "此账户已注销"
        else:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_stu.delete_time=now_time
            current_stu.is_delete=True
            current_stu.save()
            message = "注销成功"
            status = 200

    resp = {
        'status': status,
        'message': message,
    }

    return JsonResponse(resp, content_type="application/json")


