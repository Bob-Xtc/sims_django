from django.db import models

from utils.common import create_uuid
# Create your models here.


class Student(models.Model):
    """学生类"""
    # 基本信息
    uuid = models.CharField(primary_key=True,
                            default=create_uuid(),
                            max_length=50)
    student_id = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=16)
    name = models.CharField(max_length=15)
    birthday = models.DateField()
    sex = models.CharField(max_length=5)
    major = models.CharField(max_length=20)

    # 创建、注销时间
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    course = models.ManyToManyField(to="Course", 
                                    through='Course_2_Student', 
                                    through_fields=('student', 'course'))


class Teachers(models.Model):
    """老师类"""
    # 基本信息
    uuid = models.CharField(primary_key=True,
                            default=create_uuid(),
                            max_length=50)
    employee_id = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=16)
    name = models.CharField(max_length=15)
    birthday = models.DateField()
    sex = models.CharField(max_length=5)
    major = models.CharField(max_length=20)
    # rank属性值如：教授、助教之类的职级
    rank = models.CharField(max_length=10)
    
    # 创建、注销时间
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)


class Course(models.Model):
    """课程表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    major = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    
    # 开课、结课时间
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


class Course_2_Student(models.Model):
    """学生、课程关联中间表"""
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(to='Student', to_field='uuid', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(to='Course', to_field='id', on_delete=models.DO_NOTHING)

    
    
