from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views as accounts
from rest_framework import routers

router = routers.DefaultRouter()
router.register('module', accounts.ModuleView)
router.register('session', accounts.SessionView)
# router.register('restauth/', include('rest_auth.urls'))

## comment out because hyperlinked didnt work.
app_name = 'accounts'

urlpatterns = [
    path('', accounts.index, name='index' ),
    
    path('employer/signup/', accounts.employer_signup, name='employer_signup'),
    path('employer/profile/', accounts.employer_profile, name='employer_profile'),
    path('employer/employees/', accounts.employees_list, name='employees_list'),
    path('employer/dashboard/', accounts.employer_dashboard, name='employer_dashboard'),
    path('employer/add/', accounts.employee_add, name='employee_add'),
    path('employer/employees_session', accounts.session_employer_view, name='session_employer_view'),

    path('employee/profile/', accounts.employee_profile, name='employee_profile'),
    path('employee/dashboard/', accounts.employee_dashboard, name='employee_dashboard'),
    path('employee/<int:uid>/setpassword/', accounts.employee_set_password, name='employee_set_password'),
    path('employee/session', accounts.session_employee_list, name='session_employee_list'),

    path('activate/account/<slug:uidb64>/<slug:token>/', accounts.activate_account, name='activate_account'),
    path('account/activation/sent/', accounts.activation_sent, name='account_activation_sent'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login_redirect/', accounts.redirect_login, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('module/', accounts.module_create, name='module_create'),
    path('session/', accounts.session_create, name='session_create'),


    ##for api calls
    path('api/', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
]