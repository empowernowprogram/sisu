from django.conf.urls import url
from django.urls import path
from . import views
#from .views import IndexView

urlpatterns = [
    path('', views.index, name='index' ),
    # url(r'^$', views.about_sisu, name='about'),
    path('about_us', views.about_us, name='about_us'),
    path('about_us/team', views.about_team, name='about_team'),
    path('about_us/empower_now', views.about_program, name='about_program'),
    path('post/', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/(?P<pk>\d+)/publish/', views.post_publish, name='post_publish'),
    path('post/(?P<pk>\d+)/remove/', views.post_remove, name='post_remove'),
    path('post/(?P<pk>\d+)/edit/', views.post_edit, name='post_edit'),
    path('comment/(?P<pk>\d+)/approve/', views.comment_approve, name='comment_approve'),
    path('comment/(?P<pk>\d+)/remove/', views.comment_remove, name='comment_remove'),
    path('post/category/(?P<category_name>\w+)', views.post_list_by_category, name='post_list_by_category'),
    path('cases', views.post_cases, name='post_cases'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('sisu_case/category/(?P<category_name>\w+)', views.story, name='story'),
    path('sisu_case/(?P<pk>\d+)/', views.story_entry, name='story_entry'),
    path('user_details/user_id/(?P<pk>\d+)/', views.user_details, name='user_details'),
    path('likepost/', views.on_off_star, name='on_off_star'),
    path('add_comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('add_reply_to_comment', views.add_reply_to_comment, name='add_reply_to_comment'),
    path('search', views.search, name='search'),
    #url(r'^settings/user_id(?P<pk>\d+)/$', IndexView.as_view(), name='user_details'),

    path('sisu_case/category/', views.get_all_category, name='get_all_category'),
    path('enp_login/', views.login_portal, name='login_portal'),
    path('employee_progress/', views.employee_progress, name='employee_progress'),
    path('supervisor_progress/', views.supervisor_progress, name='supervisorprogress'),
    path('nonsupervisor_progress/', views.nonsupervisor_progress, name='nonsupervisorprogress'),
    path('modules/', views.modules, name='modules'),
    path('downloads/', views.downloads, name='downloads'),
    path('modules_s/', views.modules_s, name='modules_s'),
    path('downloads_s/', views.downloads_s, name='downloads_s'),
    path('employee_reg', views.employee_reg, name='employee_reg'),
    path('send_reg/', views.send_reg, name='send_reg'),
    path('reg_from_invite', views.reg_from_invite, name='reg_from_invite'),

    path('terms_conditions/', views.terms_conditions, name='t_c'),
    path('privacy_policy/', views.privacy_policy, name='p_p'),

    path('header/', views.header, name='header'),

    
    # Training Portal Authentication / Login / Logout - START
    path('auth-login/', views.portal_login, name='portal_login'),
    path('auth-logout/', views.portal_logout, name='portal_logout'),
    # Training Portal Authentication / Login / Logout - START


    # Training Portal - START
    path('portal/home/', views.portal_home, name='home_portal'),
    path('portal/register/', views.portal_register, name='register'),
    path('portal/edit-registration/', views.portal_edit_registration, name='edit-registration'),
    path('portal/downloads/', views.portal_training_dl, name='downloads'),
    path('portal/progress/', views.portal_employee_progress, name='progress'),
    path('portal/settings/', views.portal_settings, name='settings'),
    # Training Portal - END

    path('portal/test/', views.test, name='test'),
    
    

]