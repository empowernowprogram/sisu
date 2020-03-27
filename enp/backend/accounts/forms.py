from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import (User, Employer, Employee, Module, Session)

class EmployerSignupForm(UserCreationForm):
    company_name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer = True
        user.is_active = False
        user.save()

        #employer profile
        company_name = self.cleaned_data.get('company_name')
        employer = Employer.objects.create(
            user=user,
            company_name=company_name,
        )

        return user


class EmployerProfileForm(forms.ModelForm):
    company_name = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'username',)

        def save(self):
            user = super().save()
            user.employer.company_name = self.cleaned_data.get('company_name')
            user.employer.save()

            return user


class EmployeeCreationForm(forms.ModelForm):
    full_name = forms.CharField()
    
    class Meta: 
        model = User
        fields = ['username', 'email']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()

        return user

class EmployeeProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'username']
    


class ModuleCreationForm(forms.ModelForm):
    
    class Meta:
        model = Module
        fields = ['case', 'categories', 'creation_date',]

class SessionCreationForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = [
            'module_id', 'score', 'grade', 
            'pass_fail', 'ethics',
        ]
    
    def set_employee(self, employee):
        self.employee = employee
    
    @transaction.atomic
    def save(self, commit=True):
        session = super().save(commit=False)
        session.employee = self.employee 
        session.save()
        
        return session