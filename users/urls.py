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

    # PASSWORD RECOVERY URLS
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
 ]