from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import *
from .models import User, Employer, Employee, Module, Session
from .tokens import activation_token
from .decorators import employer_required, employee_required

def index(request):
    context = {}
    return render(request, 'accounts/employee/home.html', context)
    

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)

        if form.is_valid():
            user = form.save() # add employer to db with is_active as False
            
            # send employer a accout activation email
            current_site = get_current_site(request)
            subject = 'Activate Employer Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user)
            })
            user.email_user(subject, message, from_email='sisuvr.testing@gmail.com')
            
            messages.success(request, 'An accout activation link has been sent to your email: ' + user.email +
                                '. Go to your email and click the link to activate your account.')
            return redirect('accounts:login')
    else:
        form = EmployerSignupForm()
    
    return render(request, 'accounts/employer/signup.html', {'form': form})

@login_required
@employer_required
def employer_profile(request):
    user = request.user
    form = EmployerProfileForm(request.POST or None, instance=user, initial= {
        'company_name': user.employer.company_name,
    })

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('accounts:employer_profile')
    
    return render(request, 'accounts/employer/profile.html', {'form': form})

@login_required
@employer_required
def employer_dashboard(request):
    return render(request, 'accounts/employer/dashboard.html')

@login_required
@employer_required
def employees_list(request):
    employees = Employee.objects.filter(employer_id=request.user.employer)
    employees = [team.user for team in employees]

    
    return render(request, 'accounts/employer/employees.html', {
        'employees': employees,
    })


@login_required
@employer_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            field = data['full_name']

            employee = form.save(commit=False)
            employee.is_active = False
            employee.save()
            Employee.objects.create(
                user = employee,
                employer_id = request.user.employer,
                full_name = field
            )

            current_site = get_current_site(request)
            subject = 'Activate Employee Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': employee,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(employee.pk)),
                'token': activation_token.make_token(employee)
            })
            employee.email_user(subject, message, from_email='sisuvr.testing@gmail.com')

            messages.info(request, 'Employee '+employee.email+' has been added successfully and an account activation link sent to their email')
            return redirect('accounts:employee_add')
    else:
        form = EmployeeCreationForm()
    
    return render(request, 'accounts/employer/employee_add.html', {'employee_creation_form': form})


@login_required
@employee_required
def employee_profile(request):
    form = EmployeeProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your profile has been updated')
    
    return render(request, 'accounts/employee/profile.html', {'form': form})


@login_required
@employee_required
def employee_dashboard(request):
    sessions = Session.objects.filter(employee=request.user.employee)
    context = {'sessions': sessions}
    return render(request, 'accounts/employee/dashboard.html', context)

@login_required
def redirect_login(request):
    if request.user.is_employer:
        return redirect('accounts:employer_dashboard')
    return redirect('accounts:employee_dashboard')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        if user.is_employer:
            messages.success(request, 'You have successfully confirmed your email. Log in to proceed.')
            return redirect('accounts:login')
        else:
            messages.info(request, 'Set a password for your Employee account.')
            return redirect('accounts:employee_set_password', uid=user.id)
    
    # invalid link
    messages.error(request, 'Account activation link is invalid or has expired. Contact your Employer for assistance')
    return redirect('accounts:home')


def activation_sent(request):
    return HttpResponse('<p>An activation link has been sent to your email</p>')


def employee_set_password(request, uid):
    user = get_object_or_404(User, pk=uid)
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            messages.success(request, 'Welcome '+user.email+'. Your account is now operational')
            return redirect('accounts:login_redirect')
    else:
        form = SetPasswordForm(user)
    
    return render (request, 'accounts/employee/set_password.html', {'set_password_form': form, 'user': user})

@require_POST
@employer_required
@login_required
def pusher_auth(request):
    '''
    employers have only access to private-{{employer-email}} channels,
    employer-email should match the current user
    '''
    socket_id = request.POST['socket_id']
    channel_name = request.POST['channel_name']
    
    start_index = len('private-')
    employer_email = channel_name[start_index:]
    
    if request.user.email == employer_email:
        pusher_client = pusher.Pusher(
                app_id = settings.APP_ID,
                key = settings.APP_KEY,
                secret = settings.APP_SECRET,
                cluster = settings.APP_CLUSTER
            )
        
        auth = pusher_client.authenticate(
                channel = channel_name,
                socket_id = socket_id
            )
        return JsonResponse(auth)
    else:
        return HttpResponseForbidden()


def module_create(request):
    form = ModuleCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
    
    context = {'form': form}

    return render(request, 'sessions/module.html', context)


@employee_required
@login_required
def session_create(request):
    if request.method == 'POST':
        form = SessionCreationForm(request.POST)
        if form.is_valid():
            form.set_employee(request.user.employee)
            session = form.save()
            return redirect('accounts:session_create')
    else: # GET
        form = SessionCreationForm()

    return render(request, 'sessions/session_create.html', {'session': form})


@employee_required
@login_required
def session_employee_list(request):
    sessions = Session.objects.filter(employee=request.user.employee)
    context = {'sessions': sessions}

    return render(request, 'accounts/employee/session_employee.html', context)


@employer_required
@login_required
def session_employer_view(request):
    sessions_list = Session.objects.filter(employee__employer_id=request.user.employer)
    context = context = {'sessions_list': sessions_list}

    return render(request, 'accounts/employer/employees_session.html', context)

