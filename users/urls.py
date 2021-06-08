# users/urls.py
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^update_profile/(?P<pk>[\-\w]+)/$', views.display_profile, name='display_profile'),
    url(r'^updated/(?P<pk>[\-\w]+)/$', views.update_user, name='update_profile'),
    url(r'^delete/(?P<pk>[\-\w]+)/$', views.DeleteUser.as_view(), name='delete_profile'),
    
    url('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/$', views.change_password, name='change_password'),
 ]