from __future__ import unicode_literals
from .models import LinkedinPost, MediumPost, Pres
import sendgrid
import os, urllib
import requests, json
from django.template import loader
from collections import defaultdict
from datetime import timedelta
from sendgrid.helpers.mail import *
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Comment, Category, PostPreferrence, ReplyToComment,Cluster, Resource
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, ContactForm, SearchForm, ReplyToCommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import send_mail, BadHeaderError, EmailMessage, send_mail, EmailMultiAlternatives
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from ipware import get_client_ip
from django.template import Context
import re, random, math
import copy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from users.models import CustomUser, UserProfile
from users.forms import CustomUserCreationForm, UserProfileForm
from enpApi.models import PlaySession, Player, Employer, Modules, TrainingPackageDownloadLink, ComparisonRating, Adjective, SelectedAdjective, PostProgramSurvey, PostProgramSurveySupervisor
from enpApi.models import Behavior, SceneInfo, EthicalFeedback, SupervisorMapping # for ethical framework report
from django.template.loader import render_to_string
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

# from .suggestions import update_clusters

import pygal
from .chart import CatPieChart, PollHorizontalBarChart
from django.views.generic import TemplateView

from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

from datetime import date

def index(request):
    context = {}
    if request.method == 'POST':
        url = "https://api.mailerlite.com/api/v2/groups/104430287/subscribers"
        
        data = {
            'email': request.POST['email_signup']
        }
        payload = json.dumps(data)
        headers = {
            'content-type': "application/json",
            'x-mailerlite-apikey': "cdf788da5a461f34b95459a22160a4ee"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
    return render(request, 'blog/home.html', context)


def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )


# Create your views here.
def login_portal(request): 
    if request.method == 'POST':
        print('WORKING?')
    else:
        print('error')

    context = {}
    return render(request, 'auth/login.html', context)
    # return redirect('portal/home.html')


def modules(request):
    if request.user.is_authenticated:
        return render(request, 'blog/modules.html')
    else:
        return render(request, 'blog/login_portal.html')


def modules_s(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        context = { 'player': player }
        return render(request, 'blog/modules_s.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def downloads(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        context = { 'player': player }
        return render(request, 'blog/downloads.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def downloads_s(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        context = { 'player': player }
        return render(request, 'blog/downloads_s.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def reg_from_invite(request):
    if request.method == 'GET':
        code = request.GET['code']
        try:
            invite = Invite.objects.get(link=code)
            email = invite.email
            employer = invite.employer
            print (username)
        except ObjectDoesNotExist:
            print("Not found")
    return render(request, 'blog/reg_from_invite.html')


def register_new_employee(request):
    return render(request, 'blog/modules.html')


def employee_reg(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        context = { 'player': player }
        return render(request, 'blog/employee_registration.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def send_reg(request):
    return render(request, 'blog/login_portal.html')
    

def employee_progress(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        player = Player.objects.get(user=request.user)
        print (player.user.username)
        
        context = { 'player': player }
        return render(request, 'blog/employee_progress.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def nonsupervisor_progress(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        user_email = request.user.email
        players = Player.objects.filter(employer='0').filter(supervisor='False')
        #print (sessions.count)
        context = { 'players': players, 'player': player }
        return render(request, 'blog/nonsupervisor_progress.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def forgot_password(request):
    email_signup = request.Get.get('email_signup')
    #EmailList.objects.create(email = email_signup)
    #context = {'company_name': employer, 'training_type': "VR", 'training_duration': "60 Minutes", 'user': i, 'pw': "default1234", 'isSuper': 1}
    context = {'user': "Sisu VR User", 'company_name': "Sisu VR", 'key': "New Password Key"}
    #print (os.environ.get('SENDGRID_API_KEY'))  
    #sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    #print("Set sendgrid instance")
    #from_email = Email("Hello@sisuvr.com")
    #print("Set from email")
    #to_email = Email(i)
    #print("Set to email")
    #subject = "Register for the Empower Now Program from Sisu VR"
    #subject = sender + form.cleaned_data['subject']
    #print("Set subject")
    html = render_to_string('email-templates/email-forgot-password.html', context)
    #content = Content("text/html", html)
                
    #print("Creating mail structure")
    #mail = Mail(from_email, subject, to_email, content)
    #print("Attempting to send mail")
    #response = sg.client.mail.send.post(request_body=mail.get())
    message = EmailMultiAlternatives(subject, '', 'hello@sisuvr.com', [email_signup])
    message.attach_alternative(html, "text/html")
    message.send()
    return render(request, 'auth/login.html')


def recover_password(request):
    if request.method == 'POST':

        username = request.POST['username']
        #password = request.POST['password']
        usr = get_user_model().objects.filter(email = request.GET['username'])   

        emp = Employer.objects.get(company_name=request.POST['company'])

        print(emp)
        print(request.POST['isSuper'])
        if request.POST['npassword1'] == request.POST['npassword2']:
            user.set_password(npassword1)
            user.save()

    if request.method == 'GET':
        key = request.GET['key']
        if PassWordKey.objects.filter(key=key).user == request.GET['user']:
            usr = get_user_model().objects.filter(email = request.GET['user'])   
            context = {usr : request.GET['user']}
            render(request, 'auth/recover.html', context)
    return render(request, 'auth/recover.html')


def supervisor_progress(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        user_email = request.user.email
        players = Player.objects.filter(employer='0').filter(supervisor='True')
        #print (sessions.count)
        context = { 'players': players, 'player': player }
        return render(request, 'blog/supervisor_progress.html', context)
    else:
        return render(request, 'blog/login_portal.html')


def attempt_login(request):
    if request.method == 'GET':
        employee_user = request.GET['user']
        employee_password = request.GET['pass']
        user = authenticate(username=employee_user, password=employee_password)
        if user is not None:
            data = { 'valid': 'yes', 'email': user.email }
            return JsonResponse(data)
        else:
            data = { 'valid': 'no' }
            return JsonResponse(data)
    if request.method == 'POST':
        employee_user = request.POST.get("user")
        print(employee_user)
        employee_pass = request.POST.get("pass")
        print(employee_pass)
        user = authenticate(username=employee_user, password=employee_pass)
        if user is not None:
            data = { 'valid': 'yes', 'email': user.email }
            return JsonResponse(data)
        else:
            data = { 'valid': 'no' }
            return JsonResponse(data)


#
# Global variables across all templates
# 
def category(request):
  categories = Category.__members__.items()
  user_ip = get_client_ip(request)
  ip = user_ip[0]
  
  request.session['ip'] = ip
  
  if request.user.is_authenticated: 
    user = CustomUser.objects.get(pk=request.user.pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(CustomUser, UserProfile, fields=('photo',))
    formset = ProfileInlineFormset(instance=user)

    if request.user.id == user.id:
        if request.method == "POST":
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            
    return {
        'categories' : categories,
        'signup_form': CustomUserCreationForm(),
        'isLoggedIn': True,
        'userprofile': formset,
    }
  else :
    return {
        'categories' : categories,
        'signup_form': CustomUserCreationForm(),
        'isLoggedIn': False,
    }
        
# Popular cases
# list top 3 cases with the most comments
# get no. of comments for all posts
def popular_cases(request):
  cases = Comment.objects.filter(approved_comment=True).values('post').annotate(dcount=Count('post')).order_by('-dcount')
  default_cases = []
  
  if not cases.first():
    default_cases = Post.objects.filter(pk__in=[1, 2, 3])
  else:
    default_cases = []
    
  size = Post.objects.all().count();
  
  count = 0;
  pop_posts = [];
  casesparsed = {};
  
  for case in cases:
    casesparsed[case['post']] = case['dcount']
    
    if count < 3:
      #print(case['post'])
      #print(Post.objects.filter(pk=case['post']))
      pop_posts.append(Post.objects.filter(pk=case['post']))
      count = count + 1;
  
  #print(casesparsed)
  random_cases = []
  limit = len(Post.objects.all())
  if limit > 2:
    random_numbers = random.sample(range(1, limit), 2)
  elif limit > 1:
    random_numbers = [1, 2]
  elif limit > 0:
    random_numbers = [1]
  else:
    random_numbers = []
  random_cases = Post.objects.filter(pk__in=random_numbers)  
  
  return {'pop_cases' : pop_posts, 
          'cases':casesparsed, 
          'random_cases': random_cases,
          'default_cases' : default_cases}

# Recommendation
def user_recommendation_list(request):
  post_list = {}
  
#   if request.user.is_authenticated:
#     # get the user commented:
#     user_commented = Comment.objects.filter(author=request.user.username).prefetch_related('post')
#     user_metooed = PostPreferrence.objects.filter(vote_value=1, username=auth.get_user(request))
    
#     user_commented_posts = set(map(lambda x: x.post.pk, user_commented))
#     user_metooed_posts = set(map(lambda x: x.postpk.pk, user_metooed))
    
#     #print (user_commented_posts)
#     #print (user_metooed_posts)
    
#     # the set of posts this user commented and metooed
#     user_set = user_commented_posts | user_metooed_posts
#     #print (recommend_set)
    
#     #get user cluster name & get all other cluster members
#     try:
#        user_cluster = CustomUser.objects.get(username=auth.get_user(request)).cluster_set.first().name
    
#     except: # if no cluster assigned for a user, update clusters
#        update_clusters("true")
#        user_cluster = CustomUser.objects.get(username=auth.get_user(request)).cluster_set.first().name
    
#     user_cluster_other_members = Cluster.objects.get(name=user_cluster).users.exclude(username=auth.get_user(request)).all()
#     other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))
    
#     # get other users' commented and metooed posts from the same clusters
#     other_user_commented_posts = Comment.objects.filter(author__in=other_members_usernames).exclude(post__pk__in=user_set)
#     other_user_metooed_posts =  PostPreferrence.objects.filter(username__username__exact=other_members_usernames, vote_value=1).exclude(postpk__pk__in=user_set)        
    
#     other_user_commented = set(map(lambda x: x.post.pk, other_user_commented_posts))
#     other_user_metooed = set(map(lambda x: x.postpk.pk, other_user_metooed_posts))
    
#     other_users_set = other_user_commented | other_user_metooed
    
#     post_list_1 = list(Post.objects.filter(id__in=other_users_set))
#     post_list_2 = list(Post.objects.exclude(id__in=user_set))
    
#     post_list = list(set(post_list_1)|set(post_list_2))[:3]
    
    #print(post_list)
    #print(other_users_set)
    #print(other_members_usernames)
  
  return {'rec_post_list': '1'}

#
# For About us page
#



def about_sisu(request):
    context = {
        'signup_form': CustomUserCreationForm()
    }
    
    return render(request, 'blog/about.html', context)

def enp(request):
    return render(request, 'blog/enp.html')

def mindglow(request):
    return render(request, 'blog/mindglow.html')
    
def about_us(request):
    return render(request, 'blog/about-us.html')
    
def about_team(request):
    return render(request, 'blog/about_team.html')    

def about_program(request):
    return render(request, 'blog/about_program.html')    

def terms_conditions(request):
    return render(request, 'blog/terms_condition.html')
    
def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

def header(request):
    return render(request, 'blog/header.html')


def faq(request):
    return render(request, 'blog/faq.html')

def contact(request):
    if request.method == 'POST':
        # validate captcha
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
            }
        data        = urllib.parse.urlencode(values).encode()
        req         = urllib.request.Request(url, data=data)
        response    = urllib.request.urlopen(req)
        result      = json.loads(response.read().decode()) # if pass result["success"] will == True        

        if result['success'] == True:
            input_first_name    = request.POST.get('input-first-name')
            input_last_name     = request.POST.get('input-last-name')
            input_subject     = request.POST.get('input-subject')
            input_email         = request.POST.get('input-email')
            input_company_name  = request.POST.get('input-company-name')
            input_message       = request.POST.get('input-message')

            subject = f'[Contact Us] - from {str(input_first_name)} {str(input_last_name)} - {str(input_subject)}'
            emailContent = {
                'input_first_name': input_first_name,
                'input_last_name': input_last_name,
                'input_email': input_email,
                'input_company_name': input_company_name,
                'input_subject': input_subject,
                'input_message': input_message,
            }
            html_content = render_to_string('email-templates/email-contact-us.html', emailContent)

            # this is a quick fix, because for whatever reason, the "required" tag on the html page is not working.
            if len(input_first_name) != 0 and len(input_last_name) != 0 and "@" in input_email and len(input_message) != 0:
                
                try:
                    #send mail to company's email
                    mail = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [settings.DEFAULT_FROM_EMAIL])
                    mail.attach_alternative(html_content, "text/html")
                    mail.send()

                    messages.success(request, mark_safe('<strong>Message sent!</strong> Thank you for contacting Sisu VR, we will reply to you shortly!'))
                    return redirect('/contact')

                except:
                    messages.error(request, mark_safe('<strong>Error occurred.</strong> Message could not be sent due to an error. </br>If this error persists please email <strong>hello@sisuvr.com</strong> directly. Thank you!'))
                    return redirect('/contact')
            
            else:
                messages.error(request, mark_safe('<strong>Error occurred.</strong> Please make sure you filled out all required fields. </br>If this error persists please email <strong>hello@sisuvr.com</strong> directly. Thank you!'))
                return redirect('/contact')

    return render(request, 'blog/contact.html')


# Training Portal Authentication / Login, Logout - START
def portal_login(request):
    # todo - better method is to incorporate 'next=?' operations and logic
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/portal/home/')
        else:
            context = {'bad_login_is': True}
            messages.info(request, 'invalid credentials')
            # messages.info(request, 'invalid credentials')
            return render(request, 'auth/login.html', context)
    else:    
        return render(request, 'auth/login.html')
    return render(request, 'auth/login.html')
 
def portal_login_trial(request):
    # todo - better method is to incorporate 'next=?' operations and logic
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/portal/downloads_trial/')
        else:
            context = {'bad_login_is': True}
            messages.info(request, 'invalid credentials')
            # messages.info(request, 'invalid credentials')
            return render(request, 'auth/login_trial.html', context)
    else:    
        return render(request, 'auth/login_trial.html')
    return render(request, 'auth/login_trial.html')
   

def portal_logout(request):
    auth.logout(request)
    return redirect('/portal/home')


# Training Portal Authentication / Login, Logout - START
# portal_signup assign play sessions to user after clicking on the link in registration email
def portal_signup(request):
    # todo - better method is to incorporate 'next=?' operations and logic
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
    
        company = request.POST['company']
        employer = Employer.objects.get(company_name=company)

        if user is not None:
            auth.login(request, user)

            npassword1 = request.POST['npassword1']
            npassword2 = request.POST['npassword2']

            if npassword1 == npassword2:
                # validate password
                try:
                    validate_password(npassword1, user=user)
                except:
                    messages.error(request, mark_safe('<strong>Error occurred.</strong> Please make sure you followed the password rules. </br>If this error persists please email <strong>hello@sisuvr.com</strong> directly. Thank you!'))
                    return redirect('/auth-register/?user={}&cmp={}&type={}&is={}'.format(username, company, request.POST['training'], request.POST['isSuper']))

                # set new password
                user.set_password(npassword1)
                user.save()

                # create player
                newPlayer = Player.objects.create(email=username, full_name=request.POST['name'], registration_type=request.POST['training'], supervisor=request.POST['isSuper'], user=user, employer=employer)
                
                # create playsession
                allModules = employer.registered_modules.all()
                for module in allModules:
                    PlaySession.objects.create(employer=employer.employer_id, player=newPlayer, module_id=module.module_id, score=0, success=False, time_taken=0)

                return redirect('/portal/home/')
            else:
                context = {'bad_login_is' : True}
        else:
            context = {'bad_login_is': True}
            messages.info(request, 'invalid credentials')
            return render(request, 'auth/register.html', context)
    else:
        training = request.GET['type']
        company = request.GET['cmp']
        usr = request.GET['user']
        isSuper = request.GET['is']
        context = {'training': training, 'company': company, 'usr': usr, 'is': isSuper}    
        return render(request, 'auth/register.html', context)
    
    return render(request, 'auth/register.html')


def key_redeem(request):
    context = {'key': '1111-2222-3333-4444'}
    return render(request, 'auth/key-redeem.html', context)

# Training Portal Authentication / Login, Logout - END




# Training Portal - START
def check_mandatory_completion(player, play_sessions):

    company_mandatory_modules = player.employer.mandatory_modules.all()
    mandatory_modules_list = []
    print('module list: ', company_mandatory_modules)
    for module in company_mandatory_modules:
        mandatory_modules_list.append(module.module_id)

    has_completed_all_mandatory = True

    for play_session in play_sessions:
        if not play_session.success and play_session.module_id in mandatory_modules_list:
            has_completed_all_mandatory = False
            break
    
    return has_completed_all_mandatory, mandatory_modules_list


def portal_home(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        play_sessions = PlaySession.objects.filter(player=str(player)).order_by('module_id')
        play_sessions_completed = PlaySession.objects.filter(player=str(player)).filter(success=True)

        due_date = player.training_deadline or player.creation_date + timedelta(days= player.employer.deadline_duration_days)
        
        has_completed_all_mandatory, mandatory_modules_list = check_mandatory_completion(player, play_sessions)

        context = {
            'player': player, 
            'play_sessions': play_sessions, 
            'play_sessions_completed': play_sessions_completed,
            'due_date': due_date,
            'mandatory_modules_list': mandatory_modules_list,
            'has_completed_all_mandatory': has_completed_all_mandatory
            }
        
        return render(request, 'portal/home.html', context)
    else:
        return render(request, 'auth/login.html')


def split_emails(email_string):
    emails = re.split('; |;, |,| |  |\*|$|$ |\n', email_string)
    emails = list(filter(None, emails))
    return emails


# send_html_email sends email and returns True if the email is successfully sent
def send_html_email(email_templates, context, subject, email_address, from_email='hello@sisuvr.com'):
    try:
        html = render_to_string(email_templates, context)
        message = EmailMultiAlternatives(subject, '', from_email, [email_address])
        message.attach_alternative(html, "text/html")
        message.send()
        return True
    except:
        return False


def portal_register(request):

    if request.user.is_authenticated:

        player = Player.objects.get(user=request.user)
        employer = player.employer
        employer_name = employer.company_name
        due_date_by_days = employer.deadline_duration_days
         
        if request.is_ajax():
            print('request - is ajax')
            # get inputs
            emails_vr_nonsupervisor         = request.GET.get('vr_nonsupervisor')
            emails_vr_supervisor            = request.GET.get('vr_supervisor')
            emails_desktop_nonsupervisor    = request.GET.get('desktop_nonsupervisor')
            emails_desktop_supervisor       = request.GET.get('desktop_supervisor')
            print('emails_vr_nonsupervisor: ')
            print(emails_vr_nonsupervisor)

            # convert email strings to lists
            emails_vr_nonsupervisor         = split_emails(emails_vr_nonsupervisor)
            emails_vr_supervisor            = split_emails(emails_vr_supervisor)
            emails_desktop_nonsupervisor    = split_emails(emails_desktop_nonsupervisor)
            emails_desktop_supervisor       = split_emails(emails_desktop_supervisor)

            # common settings for all type of users
            default_pwd = "default1234"
            subject = "Register for the Empower Now Program from Sisu VR"
            email_templates = 'email-templates/email-training-signup.html'
            context = {'company_name': employer_name, 'due_date_by_days': due_date_by_days, 'training_duration': "60 Minutes", 'pw': default_pwd}

            failure_list = []

            # send emails for VR nonsupervisors
            for email_address in emails_vr_nonsupervisor:
                if email_address == '':
                    break

                context['user'] = email_address
                context['training_type'] = 'VR'
                context['isSuper'] = 0

                is_success = send_html_email(email_templates, context, subject, email_address)
                
                if is_success:
                    if not get_user_model().objects.filter(email=email_address).exists():
                        get_user_model().objects.create_user(username=email_address, email=email_address, password=default_pwd)
                else:
                    failure_list.append(email_address)
                
            # send emails for VR supervisors
            for email_address in emails_vr_supervisor:
                if email_address == '':
                    break

                context['user'] = email_address
                context['training_type'] = 'VR'
                context['isSuper'] = 1

                is_success = send_html_email(email_templates, context, subject, email_address)

                if is_success:
                    if not get_user_model().objects.filter(email=email_address).exists():
                        get_user_model().objects.create_user(username=email_address, email=email_address, password=default_pwd)
                else:
                    failure_list.append(email_address)

            # send emails for Desktop nonsupervisors
            for email_address in emails_desktop_nonsupervisor:
                if email_address == '':
                    break
                
                context['user'] = email_address
                context['training_type'] = 'Desktop'
                context['isSuper'] = 0

                is_success = send_html_email(email_templates, context, subject, email_address)
                
                if is_success:
                    if not get_user_model().objects.filter(email=email_address).exists():
                        get_user_model().objects.create_user(username=email_address, email=email_address, password=default_pwd)
                else:
                    failure_list.append(email_address)

            # send emails for Desktop supervisors
            for email_address in emails_desktop_supervisor:
                if email_address == '':
                    break
                
                context['user'] = email_address
                context['training_type'] = 'Desktop'
                context['isSuper'] = 1

                is_success = send_html_email(email_templates, context, subject, email_address)
                
                if is_success:
                    if not get_user_model().objects.filter(email=email_address).exists():
                        get_user_model().objects.create_user(username=email_address, email=email_address, password=default_pwd)
                else:
                    failure_list.append(email_address)
            

            context = {'status': 'success', 'failure_list': failure_list}
            return JsonResponse(context, status=200)

        context = {'player': player}
        return render(request, 'portal/register.html', context)

    else:
        return render(request, 'auth/login.html')

def portal_change_password(request):
    if request.user.is_authenticated:
        #if request.user.check_pasword(request.POST['old-password']):
            if request.POST['new-password-1'] == request.POST['new-password-2']:
                u = request.user
                u.set_password(request.POST['new-password-2'])
                u.save()
                return redirect('/portal/home/')
            else:
                return redirect('/portal/settings/')
        #else:
            #return redirect('/portal/settings')
    else:
        return render(request, 'auth/login.html')


""" Training Portal - Registration START """

def portal_edit_registration(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        players = Player.objects.filter(employer=player.employer)

        context = {'player': player, 'players': players}
        
        return render(request, 'portal/edit-registration.html', context)
            
    else:
        return render(request, 'auth/login.html')

def portal_edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_email = request.POST['userEmail1']
            user_name = request.POST['userName']
            user_registration_type = request.POST['regiTypeDropDown']
            isSupervisor = (user_registration_type == "1") # value 1 means user selected "Supervisor"
            
            Player.objects.filter(email=user_email).update(full_name=user_name, supervisor=isSupervisor)

            return redirect('/portal/edit-registration/')

    else:
        return render(request, 'auth/login.html')

def portal_remove_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_email = request.POST['userEmail2']

            # remove player (play session) and then remove user
            # a better way to do this is to have a boolean field 'disabled' to prevent data loss?
            Player.objects.filter(email=user_email).delete()

            user = CustomUser.objects.filter(email=user_email)
            user_obj = user.first()

            queryset = PostProgramSurveySupervisor.objects.filter(user=user_obj)
            if queryset.exists():
                queryset.delete()

            queryset = PostProgramSurvey.objects.filter(user=user_obj)
            if queryset.exists():
                queryset.delete()

            queryset = SelectedAdjective.objects.filter(user=user_obj)
            if queryset.exists():
                queryset.delete()

            queryset = EthicalFeedback.objects.filter(user=user_obj)
            if queryset.exists():
                queryset.delete()

            user.delete()

            return redirect('/portal/edit-registration/')

    else:
        return render(request, 'auth/login.html')

""" Training Portal - Registration END """

def portal_training_dl(request):
    if request.user.is_authenticated:
      player = Player.objects.get(user=request.user)
      if player.admin == True:
        module_download_links = TrainingPackageDownloadLink.objects.all()
            # module_download_links = module_download_links.order_by('is_supervisor')
      else:
            # non-supervisor
        if player.supervisor == False and player.registration_type == 'Desktop':
          module_download_links = TrainingPackageDownloadLink.objects.filter(training_type='Desktop', is_supervisor=False)
        elif player.supervisor == False and player.registration_type == 'VR':
          module_download_links = TrainingPackageDownloadLink.objects.filter(training_type='VR', is_supervisor=False)
        elif player.supervisor == True and player.registration_type == 'Desktop':
          module_download_links = TrainingPackageDownloadLink.objects.filter(training_type='Desktop', is_supervisor=True)
        elif player.supervisor == True and player.registration_type == 'VR':
          module_download_links = TrainingPackageDownloadLink.objects.filter(training_type='VR', is_supervisor=True)
        else:
          module_download_links = ''

      print(module_download_links)
      context = {'player': player, 'module_download_links': module_download_links}
      return render(request, 'portal/downloads.html', context)
    else:
      return render(request, 'auth/login.html')


def portal_training_dl_trial(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        context = {'player': player}
        return render(request, 'portal/downloads_trial.html', context)
    else:
        return render(request, 'auth/login.html')


def portal_employee_progress(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        
        if player.admin:
            # show all players in this company
            players = Player.objects.filter(employer=player.employer)
            play_sessions = PlaySession.objects.filter(employer=player.employer.employer_id)

        elif player.supervisor:
            # show this supervisor's team result
            thisTeamUsers = SupervisorMapping.objects.filter(supervisor=request.user).values_list('employee', flat=True)
            players = Player.objects.filter(user__in=thisTeamUsers)
            play_sessions = PlaySession.objects.filter(player__in=players)
        
        else:
            return redirect('/portal/home/')

        players_obj = []

        # creating dictionary with aggregated data to be rendered to DOM.
        # reason for doing this is because quantity of modules completed player are from two different data sets and require looping
        for i, player_single in enumerate(players):
            if player_single.supervisor: 
                registration_type = 'Supervisor' 
            else: 
                registration_type = 'Non-supervisor'

            all_modules = play_sessions.filter(player=player_single)
            completed_modules = play_sessions.filter(player=player_single).filter(success=True)

            players_obj.append({
                'name': player_single.full_name,
                'email': player_single.email,
                'registration': registration_type,
                'all_modules': len(all_modules),
                'modules_completed': len(completed_modules),
                'date': date.today()
            })
        
        context = {'player': player, 'players_obj': players_obj}
        
        return render(request, 'portal/progress.html', context)
    else:
        return render(request, 'auth/login.html')


def portal_settings(request):

    if request.user.is_authenticated:

        player = Player.objects.get(user=request.user)

        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings')

            else:
                messages.error(request, mark_safe('<strong>Error occurred.</strong> Please make sure you filled out all required fields and followed the password rules. </br>If this error persists please email <strong>hello@sisuvr.com</strong> directly. Thank you!'))

        else:
            form = PasswordChangeForm(request.user)
        

        context = {
            'player': player,
            'form': form
            }

        return render(request, 'portal/settings.html', context)

    else:
        return render(request, 'auth/login.html')


def portal_certificate(request):
    if request.user.is_authenticated:
        player = Player.objects.get(user=request.user)
        play_sessions = PlaySession.objects.filter(player=str(player)).order_by('module_id')
        play_sessions_completed = PlaySession.objects.filter(player=str(player)).filter(success=True)
        company = player.employer.company_name
        logoLink = player.employer.logo

        has_completed_all_mandatory, mandatory_modules_list = check_mandatory_completion(player, play_sessions)

        date = None
        for session in play_sessions_completed:
            if not date or session.date_taken > date:
                date = session.date_taken

        context = {
            'player': player,
            'has_completed_all_mandatory': has_completed_all_mandatory,
            'company': company, 
            'logo': logoLink,
            'date': date
            }
    
        return render(request, 'portal/certificate.html', context)
    else:
        return render(request, 'auth/login.html')


def getColor(behavior):
    colorDict = {"hostile": '#FF6464',
                 "passive": '#FFBE3F', "confident": '#77B447'}

    return colorDict[behavior]


def portal_ethical_report(request, pk):
    if request.user.is_authenticated:

        player = Player.objects.get(user=request.user)
        play_sessions = PlaySession.objects.filter(player=str(player)).order_by('module_id')

        has_completed_all_mandatory, mandatory_modules_list = check_mandatory_completion(player, play_sessions)

        if not has_completed_all_mandatory:
            return render(request, 'portal/ethical-report.html', {"completedTraining": False})


        # supervisor can view aggregated report; non-supervisors and admins do not have the options
        if  pk == "team_report" :
            if player.supervisor and not player.admin:
                # filter team and aggregate data
                print('SUPERVISOR !')
                thisTeamMembers = SupervisorMapping.objects.filter(supervisor=request.user).values_list('employee', flat=True)
                queryset = EthicalFeedback.objects.filter(user__in=thisTeamMembers)

                # calulate average emotion value for each scene
                feedbackCountInModule = defaultdict(lambda: defaultdict(int)) # {module nb: {scene nb: count of feedbacks}}
                emotionSumInModule = defaultdict(lambda: defaultdict(int)) # {module nb: {scene nb: sum of employees' emotion}}
                behaviorCountInModule = defaultdict(lambda: defaultdict(dict)) # {module nb: {hostile: {scene nb: count}, ...}}
                for entry in queryset:
                    emotionSumInModule[entry.module_id][entry.scene] += entry.emotion
                    feedbackCountInModule[entry.module_id][entry.scene] += 1
                    behaviorCountInModule[entry.module_id][entry.behavior_id.description][entry.scene] = behaviorCountInModule[entry.module_id][entry.behavior_id.description].get(entry.scene, 0) + 1

                # aggregate data by module
                moduleCnt = len(emotionSumInModule)
                avgEmotionsInModule = {}
                employeeCntInModule = {}
                sceneLabelsInModule = {}
                rolesInModule = {}
                isMandatoryInModule = {}
                screenshotsInModule = {}
                npcsInModule = {}
                scriptsInModule = {}
                datasets = defaultdict(dict)

                for moduleId, emotionSum in emotionSumInModule.items():
                    sceneInfoQueries = SceneInfo.objects.filter(module_id=moduleId)
                    sceneCnt = sceneInfoQueries.count() # get scene count from scene info table

                    employeeCnt = queryset.filter(module_id=moduleId).order_by().values_list('user').distinct().count()

                    avgEmotions = [0] * sceneCnt

                    behaviorCount = behaviorCountInModule[moduleId]

                    for behavior in behaviorCount:
                        sceneData = [0] * sceneCnt
                        for scene, emoSum in emotionSum.items():
                            behaviorPercentage = behaviorCount[behavior].get(scene, 0) / feedbackCountInModule[moduleId][scene]
                            avgEmotion = emoSum / feedbackCountInModule[moduleId][scene]

                            avgEmotions[scene-1] = math.floor(avgEmotion*10)/10
                            sceneData[scene-1] = avgEmotion * behaviorPercentage

                        datasets[behavior][moduleId] = sceneData[:]


                    employeeCntInModule[moduleId] = int(employeeCnt)
                    avgEmotionsInModule[moduleId] = avgEmotions[:]
                    sceneLabelsInModule[moduleId] = list(range(1, sceneCnt+1))


                    roles = {}
                    isMandatory = {}
                    screenshots = {}
                    npcs = {}
                    scripts = {}

                    for obj in sceneInfoQueries:
                        roles[obj.scene-1] = obj.player_role
                        isMandatory[obj.scene-1] = obj.is_mandatory
                        screenshots[obj.scene-1] = obj.ethical_screenshot
                        npcs[obj.scene-1] = obj.ethical_npc_name
                        scripts[obj.scene-1] = obj.ethical_script

                    rolesInModule[moduleId] = roles
                    isMandatoryInModule[moduleId] = isMandatory
                    screenshotsInModule[moduleId] = screenshots
                    npcsInModule[moduleId] = npcs
                    scriptsInModule[moduleId] = scripts

                modules = sorted(list(emotionSumInModule.keys()))
                print(emotionSumInModule)
                print(modules)
                print(len(thisTeamMembers))

                context = {
                    'isAggregatedReport': pk == "team_report",
                    'completedTraining': True,
                    'player': player, 
                    'modules': modules,
                    'labels': sceneLabelsInModule,
                    'hostile_dataset': datasets['hostile'],
                    'passive_dataset': datasets['passive'],
                    'confident_dataset': datasets['confident'],
                    'hostile_color': getColor('hostile'),
                    'passive_color': getColor('passive'),
                    'confident_color': getColor('confident'),
                    'roles': rolesInModule,
                    'is_mandatory_scene': isMandatoryInModule,
                    'avgEmotions': avgEmotionsInModule,
                    'employeeCnt': employeeCntInModule,
                    'screenshots': screenshotsInModule,
                    'npcs': npcsInModule,
                    'scripts': scriptsInModule,
                    'moduleCnt':moduleCnt 
                }
               
            else:
                #redirect non-supervisors and supervisors to my_report route instead
                return redirect("ethical_report", pk = "my_report")
        # individual report
        elif pk == "my_report":
            
            username = request.user.username

            scenesInModules = {}
            sceneIndicesInModules = {}
            emotionsInModules = {}
            behaviorsInModules = {}
            rolesInModule = {}
            screenshotsInModule = {}
            npcsInModule = {}
            scriptsInModule = {}
            
            # when the user is either a supervisor or non-supervisor and access my_report
            if not player.admin:
                for field in play_sessions.all():
                    if not field.success:
                        continue
                        
                    moduleId = field.module_id

                    # fetch ethical feedbacks in this module
                    scenes = []
                    emotions = []
                    behaviors = []

                    queryset = EthicalFeedback.objects.filter(user__username=username).filter(module_id=moduleId)

                    for column in queryset:
                        scenes.append(column.scene)
                        emotions.append(column.emotion)
                        behaviors.append(column.behavior_id.description)
                    
                    # sort according to scene id
                    sortedData = list(sorted(zip(scenes, emotions, behaviors)))
                    scenes = list(map(lambda x: x[0], sortedData))
                    emotions = list(map(lambda x: x[1], sortedData))
                    behaviors = list(map(lambda x: x[2], sortedData))
                    
                    scenesIdices = {}
                    for i, scene in enumerate(scenes):
                        scenesIdices[scene-1] = i

                    # fetch player roles in this module
                    sceneInfoQueries = SceneInfo.objects.filter(module_id=moduleId)
                    roles = {}
                    screenshots = {}
                    npcs = {}
                    scripts = {}
                    for obj in sceneInfoQueries:
                        roles[obj.scene-1] = obj.player_role
                        screenshots[obj.scene-1] = obj.ethical_screenshot
                        npcs[obj.scene-1] = obj.ethical_npc_name
                        scripts[obj.scene-1] = obj.ethical_script

                    # store scene, emotion, behaviors, roles by module
                    scenesInModules[moduleId] = scenes
                    sceneIndicesInModules[moduleId] = scenesIdices
                    emotionsInModules[moduleId] = emotions
                    behaviorsInModules[moduleId] = behaviors
                    rolesInModule[moduleId] = roles
                    screenshotsInModule[moduleId] = screenshots
                    npcsInModule[moduleId] = npcs
                    scriptsInModule[moduleId] = scripts

                modules = sorted(list(rolesInModule.keys()))

                # colors for bars
                colors = []
                for b in behaviors:
                    colors.append(getColor(b))

                context = {
                    'isAggregatedReport': pk == "team_report",
                    'completedTraining': True,
                    'player': player,
                    'modules': modules,
                    'roles': rolesInModule,
                    'scenes': scenesInModules,
                    'scenesIdices': sceneIndicesInModules, 
                    'emotions': emotionsInModules, 
                    'behaviors': behaviorsInModules, 
                    'hostile_color': getColor('hostile'),
                    'passive_color': getColor('passive'),
                    'confident_color': getColor('confident'),
                    'screenshots': screenshotsInModule,
                    'npcs': npcsInModule,
                    'scripts': scriptsInModule,
                }
            else:
                # filter team and aggregate data
                thisCompanyMembers = Player.objects.filter(employer=player.employer).values_list('user', flat=True)
                print(thisCompanyMembers)
                queryset = EthicalFeedback.objects.filter(user__in=thisCompanyMembers)
                print(queryset)
                thisTeamMembers = SupervisorMapping.objects.filter(supervisor=request.user).values_list('employee', flat=True)
                #queryset = EthicalFeedback.objects.filter(user__in=thisTeamMembers)

                # calulate average emotion value for each scene
                feedbackCountInModule = defaultdict(lambda: defaultdict(int)) # {module nb: {scene nb: count of feedbacks}}
                emotionSumInModule = defaultdict(lambda: defaultdict(int)) # {module nb: {scene nb: sum of employees' emotion}}
                behaviorCountInModule = defaultdict(lambda: defaultdict(dict)) # {module nb: {hostile: {scene nb: count}, ...}}
                playerRolesBehaviors = defaultdict(lambda: defaultdict(int)) # {module nb: {hostile: {scene nb: count}, ...}}
                behaviorCountof = {}
                playerRoleCountof = defaultdict(int)
                playerRoleCountPercent = defaultdict(list)
                
                for entry in queryset:
                    player_role = SceneInfo.objects.filter(module_id=entry.module_id, scene=entry.scene).values_list('player_role', flat=True)[0]
                    print(player_role)
                    
                    
                    playerRolesBehaviors[entry.behavior_id.description][player_role] += 1 
                    emotionSumInModule[entry.module_id][entry.scene] += entry.emotion
                    feedbackCountInModule[entry.module_id][entry.scene] += 1
                    behaviorCountInModule[entry.module_id][entry.behavior_id.description][entry.scene] = behaviorCountInModule[entry.module_id][entry.behavior_id.description].get(entry.scene, 0) + 1
                    behaviorCountof[entry.behavior_id.description] = 0
                
                # aggregate data by module
                # print("emotion sum:", emotionSumInModule)
                
                # aggregate data by module
                moduleCnt = len(emotionSumInModule)
                sceneInfoPlayerRoles = SceneInfo.objects.all().values('player_role')
                
                avgEmotionsInModule = {}
                employeeCntInModule = {}
                LabelsInChart = {'pie':list(behaviorCountof.keys()), "bar":[playerRole['player_role'] for playerRole in sceneInfoPlayerRoles.distinct()]}
                rolesInModule = {}
                isMandatoryInModule = {}
                screenshotsInModule = {}
                npcsInModule = {}
                scriptsInModule = {}
                datasets = defaultdict(dict)
                
                print("player roles: ")
                print(sceneInfoPlayerRoles)
                print("Labels: ")
                print(LabelsInChart)
                print('emotion sum: ')
                print(emotionSumInModule)
                playerRolesBehaviors_copy = copy.deepcopy(playerRolesBehaviors)
                for behavior, behaviorCnt in playerRolesBehaviors.items():
                    print(behaviorCnt)
                    playerRolesBehaviors_copy[behavior] = list(dict(playerRolesBehaviors[behavior]).values())
                    behaviorCountof[behavior] += sum(behaviorCnt.values())
                    
                    for player_role, count in behaviorCnt.items():
                        playerRoleCountof[player_role] += count
                        
                for behavior, behaviorCnt in playerRolesBehaviors_copy.items():
                    print(behaviorCnt)
                    for i in range(len(behaviorCnt)):
                        playerRolesBehaviors_copy[behavior][i] = round(playerRolesBehaviors_copy[behavior][i] / list(playerRoleCountof.values())[i] * 10, 2) 
                playerRolesBehaviors_copy = dict(playerRolesBehaviors_copy)    
                behaviorCountof = dict(behaviorCountof)
                playerRoleCountof = dict(playerRoleCountof)      
                modules = sorted(list(emotionSumInModule.keys()))
                print("behavior count for each player role:", playerRolesBehaviors)
                print("behavior count for each player role copy:", playerRolesBehaviors_copy)
                print(playerRoleCountof)
                print(behaviorCountof)
                print(playerRoleCountPercent)

                context = {
                    'isAggregatedReport': pk == "team_report",
                    'completedTraining': True,
                    'player': player, 
                    'modules': modules,
                    'labels': LabelsInChart,
                    'hostile_color': getColor('hostile'),
                    'passive_color': getColor('passive'),
                    'confident_color': getColor('confident'),
                    #'roles': rolesInModule,
                    #'is_mandatory_scene': isMandatoryInModule,
                    #'avgEmotions': avgEmotionsInModule,
                    #'employeeCnt': employeeCntInModule,
                    'screenshots': screenshotsInModule,
                    'npcs': npcsInModule,
                    #'scripts': scriptsInModule,
                    'behaviorCountOf': behaviorCountof,
                    'playerRolesBehaviors': playerRolesBehaviors_copy,
                    'behaviorCountof':behaviorCountof,
                    'playerRoleCountof' : playerRoleCountof
                }

        return render(request, 'portal/ethical-report.html', context)
    else:
        return render(request, 'auth/login.html')

def post_program_survey(request, pk):
    isSupervisor = Player.objects.get(user=request.user).supervisor

    if pk == "supervisor" and isSupervisor:
        # show certificate if user already completed the survey
        if PostProgramSurveySupervisor.objects.filter(user=request.user).count() == 1:
            return redirect('/portal/certificate/')

        else:
            scale5 = range(1,6)
            scale10 = range(1,11)
            experienceFeatures = Adjective.objects.order_by('adj_id').values('description')
            preference = ComparisonRating.objects.order_by('comparison_rating_id').values('description')
            
            context = {'scale5': scale5, 'scale10': scale10, 'experienceFeatures': experienceFeatures, 'preference': preference}

            return render(request, 'portal/post-program-survey-supervisor.html', context)

    elif pk == "nonsupervisor" and not isSupervisor:
        # show certificate if user already completed the survey
        if PostProgramSurvey.objects.filter(user=request.user).count() == 1:
            return redirect('/portal/certificate/')

        else:
            starRange = range(1, 6)
            experienceFeatures = Adjective.objects.order_by('adj_id').values('description')
            preference = ComparisonRating.objects.order_by('comparison_rating_id').values('description')
            
            context = {'starRange': starRange, 'experienceFeatures': experienceFeatures, 'preference': preference}
            
            return render(request, 'portal/post-program-survey.html', context)
    
    else:
        return redirect('/portal/home/')


def save_survey(request, pk):
    isSupervisor = Player.objects.get(user=request.user).supervisor

    if request.method == 'POST':
        if pk == "supervisor" and isSupervisor:
            postProgramSurvey = PostProgramSurveySupervisor()

            postProgramSurvey.recommend_friend_scale = request.POST.get('recommendScore')
            postProgramSurvey.recommend_friend_reason = request.POST.get('recommendFriendReason')
            postProgramSurvey.info_retention_scale = request.POST.get('retainScore')
            postProgramSurvey.confidence_scale = request.POST.get('confidenceScore')
            postProgramSurvey.recommend_manager_scale = request.POST.get('recommendManagerScore')
            postProgramSurvey.recommend_employee_scale = request.POST.get('recommendEmployeeScore')

        elif pk == "nonsupervisor" and not isSupervisor:
            postProgramSurvey = PostProgramSurvey()

            postProgramSurvey.overall_rating = request.POST.get('overallStars')
            postProgramSurvey.overall_feedback = request.POST.get('overallFeedback')
            postProgramSurvey.contact = request.POST.get('contact')

        else:
            return redirect('/portal/home/')


        # common fields for both nonsupervisor / supervisor
        postProgramSurvey.user = request.user
        postProgramSurvey.comments = request.POST.get('comments')

        if request.POST.get('preference'):
            postProgramSurvey.comparison_rating_id = ComparisonRating.objects.get(comparison_rating_id=request.POST.get('preference'))

        postProgramSurvey.has_completed = True
        postProgramSurvey.save()

        # record the selected adjective from user (both supervisor and nonsupervisor have this question)
        selectedAdj = SelectedAdjective(user=request.user)
        selectedAdj.save()

        for adjId in request.POST.getlist('features'):
            selectedAdj.adj_id.add(Adjective.objects.get(adj_id=adjId))

        return render(request, 'portal/save-survey.html')

    else:
        return redirect('/portal/home/')

# Training Portal - END



def story(request, category_name):
    # print(pretty_request(request))
    posts = Post.objects.filter(category_name=category_name).order_by('-published_date')
    cat = Category.get_label(category_name)   
    mapping = {}
  
    # Bad hard codes...
    mapping[Category.Harassment] = "An unpleasant or hostile situation created by uninvited and unwelcome verbal or physical conduct"
    mapping[Category.Discrimination] = "The unjust or prejudicial treatment of different categories of persons, especially on the grounds of race, age, or sex"
    mapping[Category.Politics] = "Devious or divisive activity aimed at improving the status of one or more persons in an organization"
    mapping[Category.Conflict] = "A serious disagreement or argument between persons of similar age, status, or abilities"
    mapping[Category.Miscellaneous] = "Additional cases which do not fall under a particular category"   
    return render(request, 'blog/story.html', {'posts':posts, 'cat':cat, 'description': mapping[cat]})
    

def get_all_category(request):
    return render(request, 'blog/story_cat_main.html')    

   
def story_entry(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_name = auth.get_user(request)
    ip = request.session['ip']
    
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)    
    
    #print ("hit---- " + str(hit_count_response.hit_message))
    
    # Get resources
    random_num = []
    random_res = []
    res = Resource.objects.filter(category_name=post.category_name)
    random_num = list(map(lambda x: x.pk, res))
    
    limit = len(res)
    
    if limit > 2:
        random.shuffle(random_num)
        random_num = random_num[:3]
        
    if(random_num): 
        random_res = Resource.objects.filter(pk__in=random_num)
        
    #print(random_num)
    
    if request.user.is_authenticated:
        if PostPreferrence.objects.filter(username=user_name, ip_address=ip, postpk=pk, vote_value=1).exists():   
            voted = True
        else:
            voted = False
        
    else:
        if PostPreferrence.objects.filter(ip_address=ip, postpk=pk, vote_value=1).exists(): 
            voted = True
        else:
            voted = False   
    try:
        total_yes = PostPreferrence.objects.filter(vote_value=1, postpk=pk).count()
    except PostPreferrence.DoesNotExist:
        total_yes = 0;
        
    
    summary = ({
        'voted':voted,
        'total_yes': total_yes,

    }) 
    
    return render(request, 'blog/story_entry.html', 
                  {'post': post, 
                   'summary': summary,
                   'resources': random_res,
                  })    


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    return render(request, 'blog/post_list.html', {'posts':posts})
    
# Post.objects.get(pk=pk)
def post_cases(request):
    return render(request, 'blog/post_category_main.html')
    
def post_list_by_category(request, category_name):
    posts = Post.objects.filter(category_name=category_name).order_by('-published_date')
    cat = Category.get_label(category_name)
    return render(request, 'blog/post_list.html', {'posts':posts, 'cat':cat })
   
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required   
def post_draft_list(request):
  posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
  return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required  
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish_post()
    return redirect('post_detail', pk=pk)

@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required     
def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# @login_required     
# def add_comment_to_post(request):
  
#   if request.method == "GET":
#      pid = request.GET['pid']
#      author = request.GET['author']
#      content = request.GET['text']
     
#      commentpost = get_object_or_404(Post, pk=pid)
     
#      comment = Comment()
#      comment.post = commentpost
#      comment.author = author
#      comment.user = request.user
     
#      userprofile = get_object_or_404(UserProfile, user=comment.user)
#      comment.userprofile = userprofile
     
#      comment.text = content
     
#      comment.save()
    
#      update_clusters("false")
           
#   else:
#      form = CommentForm()
    
#   return render(request, 'blog/story_entry.html', {'post':commentpost})    
    
@login_required     
def add_reply_to_comment(request):
    
    if request.method == "GET":
        pid = request.GET['pid']
        cid = request.GET['cid']
        author = request.GET['author']
        content = request.GET['text']
        
        replypost = get_object_or_404(Post, pk=pid)
        comment = get_object_or_404(Comment, post=replypost, pk=cid)
        
        replyToComment = ReplyToComment()
        replyToComment.post = replypost
        replyToComment.comment = comment
        replyToComment.author = author
        replyToComment.text = content
        replyToComment.user = request.user
     
        userprofile = get_object_or_404(UserProfile, user=replyToComment.user)
        replyToComment.userprofile = userprofile
        
        replyToComment.save()
           
        data = {
            'success': True,
            'newReply': replyToComment.created_date
        }
    else:
        form = CommentForm()
    return JsonResponse(data)
    #return render(request, 'blog/story_entry.html', {'post':replypost})
    
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('story_entry', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('story_entry', pk=comment.post.pk)
#
# For contact us page
#
def contact_us(request):
    print( "Inside contact_us block")
    if request.method == 'GET':
        print("Registering as GET")
        form = ContactForm()
    else:
        print("Registering as POST")
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form is valid");
            sender = "From " + form.cleaned_data['your_name']
            if request.user.is_authenticated:
              sender = sender + "_(REG_User)_" + auth.get_user(request).username
            else:
              sender = sender + "_(PUB_User)_"
              
            print (os.environ.get('SENDGRID_API_KEY'))  
            sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            print("Set sendgrid instance")
            from_email = Email(form.cleaned_data['your_email'])
            print("Set from email")
            to_email = Email("Hello@sisuvr.com")
            print("Set to email")
            company = sender + form.cleaned_data['your_company']
            #company = form.cleaned_data['your_company']
            print("Set company")
            subject = company + form.cleaned_data['subject']
            #subject = sender + form.cleaned_data['subject']
            print("Set subject")
            content = Content("text/plain", form.cleaned_data['message'])
            print("Creating mail structure")
            mail = Mail(from_email, subject, to_email, content)
            print("Attempting to send mail")
            response = sg.client.mail.send.post(request_body=mail.get())

            '''print(response.status_code)
            print(response.body)
            print(response.headers) 
            '''
            '''
            from_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
                '''
            # return render(request, 'blog/contact_us_success.html')
            print("Sent mail!")
            context = {}
            return render(request, 'blog/home.html', context)
        print("Form is invalid")
    return render(request, "blog/contact_us.html", {'form': form})
           
   
# def on_off_star(request):

#    if request.method == 'GET':
#       post_id = request.GET['postid']
#       post_preference = request.GET['on_off_value']
#       user_name = auth.get_user(request)
#       ip = request.session['ip']
#       likedpost = get_object_or_404(Post, pk=post_id)
   
#       voted = True
#       try:
#         if request.user.is_authenticated:
#           postpreferrence_obj = PostPreferrence.objects.get(username=user_name, postpk=likedpost, ip_address=ip)     
#         else:
#           postpreferrence_obj = PostPreferrence.objects.get(postpk=likedpost, ip_address=ip)
        
#         postpreferrence_obj.vote_value = post_preference
#         postpreferrence_obj.save()    
                
        
#       except PostPreferrence.DoesNotExist:
#         post_voted = PostPreferrence()
#         post_voted.ip_address = ip
#         post_voted.postpk = likedpost
#         post_voted.vote_value = post_preference 
      
#         if request.user.is_authenticated:
#           #print("===================================" + str(user_preference) + str(ip) + str(user_name))
#           post_voted.username = user_name
#         else:
#           post_voted.username = None
          
#         post_voted.save()   
#         voted = True
   
#       summary = ({
#          'voted':voted,
#          'total_yes': PostPreferrence.objects.filter(vote_value=1, postpk=post_id).count(),
#       })
      
#       update_clusters("false")
      
#    return render(request, 'blog/story_entry.html', {'post':likedpost, 'summary':summary})   
   #return render(request, 'blog/post_detail_index.html', {'post':likedpost, 'summary':summary})   
 
# Search Functionality
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
 
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
    
def search(request):
    query_string = ''
    found_entries = None
    
    if request.method == "POST":
       search_form = SearchForm(request.POST)
      
       if search_form.is_valid():
          query_string = search_form.cleaned_data['search_string']
          post_query = get_query(query_string, ['title', 'text', 'category_name'])
          found_entries = Post.objects.filter(post_query).order_by('-published_date')
            
    else:
       search_form = SearchForm()
    
    return render(request, 'blog/post_search_res.html',{ 'query_string': query_string, 'found_entries': found_entries })
###

#
# For User Settings
#
@login_required
def user_profile(request, pk):
    user = CustomUser.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(CustomUser, UserProfile, fields=('photo',))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return render(request, "blog/user_settings_profile_upd.html")
            
            
        return render(request, "blog/user_settings.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
    #return render(request, 'blog/user_settings.html')

@login_required
def user_details(request, pk):
    user = CustomUser.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(CustomUser, UserProfile, fields=('photo',))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return render(request, "blog/user_settings_profile_upd.html")
            
            
        return render(request, "blog/user_details.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied

def user_edit(request, pk): 

    return render(request, "blog/user_edit.html", { 'isValid': True })

## Pie chart
class IndexView(TemplateView):
      template_name = 'blog/user_details.html'
      
      def get_context_data(self, **kwargs):
          context = super(IndexView, self).get_context_data(**kwargs)
          user = self.request.user
          
          user_comments_approve = Comment.objects.filter(approved_comment=True, author=user).order_by('-created_date')
          user_comments_pending = Comment.objects.filter(approved_comment=False, author=user).order_by('-created_date')
          user_metooed = PostPreferrence.objects.filter(vote_value=1, username=user).order_by('-vote_date')
    
          user_comments = user_comments_approve | user_comments_pending
          
          # Get user profile info
          cus_user = CustomUser.objects.get(pk=user.pk)
          user_form = UserProfileForm(instance=cus_user)

          ProfileInlineFormset = inlineformset_factory(CustomUser, UserProfile, fields=('photo',))
          formset = ProfileInlineFormset(instance=cus_user)
          
          user_data = []
          for comment in user_comments:
            user_data.append(comment.post)
          
          for metoo in user_metooed:
            user_data.append(metoo.postpk)
          
          if len(user_data) != 0:
            cat_chart = CatPieChart(
                          height = 600,
                          width = 800,
                          explicit_size=True,
                          )
                          
            context['cat_chart'] = cat_chart.generate(user_data)
          
          else:
            context['cat_chart'] = None
          
          context['user_commented_size'] = len(user_comments_approve)
          context['user_pending_size'] = len(user_comments_pending)
          context['user_metooed_size'] = len(user_metooed)
          context['user_commented'] = user_comments_approve[:20]
          context['user_pending'] = user_comments_pending[:20]
          context['user_metooed'] = user_metooed
          context['noodle_form'] = user_form
          context['formset'] = formset
          
          return context
def news_view(request, *args, **kwargs): 



    latest_linked_in_post_list = LinkedinPost.objects.order_by('-pub_date')[:3]
    latest_medium_post_list = MediumPost.objects.order_by('-pub_date_m')[:4]
    latest_pres_post_list = Pres.objects.order_by('-pub_date_p')[:4]

    template = loader.get_template('blog/news.html')
    context = {
        'latest_linked_in_post_list': latest_linked_in_post_list,
        'latest_medium_post_list': latest_medium_post_list,
        'latest_pres_post_list': latest_pres_post_list
    }
    for post in latest_medium_post_list:
         print(post.m_photo.url)
    
    for post in latest_pres_post_list:
         print(post.p_photo.url)

    return HttpResponse(template.render(context, request))







    return render(request, 'blog/news.html')




def handle400(request, exception):
    return render(request, 'blog/statuscode/401.html')


def handle403(request, exception):
    return render(request, 'blog/statuscode/403.html')


def handle404(request, exception):
    return render(request, 'blog/statuscode/404.html')


def handle500(request, *args, **argv):
    return render(request, 'blog/statuscode/500.html')
