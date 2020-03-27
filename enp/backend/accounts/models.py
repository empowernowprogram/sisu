from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import date
from django.utils import timezone
from shortuuidfield import ShortUUIDField

class User(AbstractUser):
    username = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=200, blank=True, unique=True)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, default=None)
    uuid = ShortUUIDField(unique=True, primary_key=True)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, default=None)
    uuid = ShortUUIDField(unique=True, primary_key=True)



class Module(models.Model):

    CATEGORIES_CHOICES = (
        ('Cat 1', 'Cat 1'),
        ('Cat 2', 'Cat 2'),
        ('Cat 3', 'Cat 3'),
        ('Cat 4', 'Cat 4'),
    )

    case = models.CharField(max_length=100)
    categories = models.CharField(max_length=6, choices=CATEGORIES_CHOICES, default='Cat 1')
    creation_date = models.DateTimeField() #need to change later

    def __str__(self):
        return self.case

class Session(models.Model):

    GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    )

    PF_CHOICES = (
        ('Passed', 'Passed'),
        ('Failed', 'Failed')
    )

    ETHIC_CHOICES = (
        ('Ethic 1', 'Ethic 1'),
        ('Ethic 2', 'Ethic 2'),
        ('Ethic 3', 'Ethic 3'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.DO_NOTHING)
    date_taken = models.DateTimeField(default=timezone.now)
    score = models.CharField(max_length=3)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, default='A')
    pass_fail = models.CharField(max_length=6, choices=PF_CHOICES, default='Passed')
    ethics = models.CharField(max_length=7, choices=ETHIC_CHOICES, default='Ethic 1')

    def __str__(self):
        return self.employee.full_name + ' ' + self.score