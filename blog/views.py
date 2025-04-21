from __future__ import unicode_literals
from .models import PressArticle, MediumPost, LinkedinPost
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



def index(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email_signup', '')

        # Check if "@" is present
        if "@" in email:
            url = "https://api.mailerlite.com/api/v2/groups/104430287/subscribers"
            data = { 'email': email }
            payload = json.dumps(data)
            headers = {
                'content-type': "application/json",
                'x-mailerlite-apikey': "cdf788da5a461f34b95459a22160a4ee"
            }
            response = requests.request("POST", url, data=payload, headers=headers)

            context['message'] = "Thanks for signing up!"
        else:
            context['error'] = "Please include an ‘@’ in the email address."

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
    
def nocode(request):
    return render(request, 'blog/nocode.html')

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
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # validate captcha
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())  # if pass result["success"] will == True

        if result['success'] == True:
            input_first_name = request.POST.get('input-first-name')
            input_last_name = request.POST.get('input-last-name')
            input_subject = request.POST.get('input-subject')
            input_email = request.POST.get('input-email')
            input_company_name = request.POST.get('input-company-name')
            input_message = request.POST.get('input-message')
            input_phone = request.POST.get('input-phone')  # Retrieve phone number

            errors = {}  # Initialize errors dictionary

            if not input_subject:
                errors['input_subject'] = ['Please select a subject.']
            if not input_first_name:
                errors['input_first_name'] = ['This field is required.']
            if not input_last_name:
                errors['input_last_name'] = ['This field is required.']
            if not input_email:
                errors['input_email'] = ['This field is required./Please add an @ in the email address.']

            if errors:
                return render(request, 'blog/contact.html', {'errors': errors, 'form_data': request.POST})
                # return render(request, 'blog/contact.html', {'errors': errors})

            subject = f'[Contact Us] - from {str(input_first_name)} {str(input_last_name)} - {str(input_subject)}'
            emailContent = {
                'input_first_name': input_first_name,
                'input_last_name': input_last_name,
                'input_email': input_email,
                'input_company_name': input_company_name,
                'input_subject': input_subject,
                'input_message': input_message,
                'input_phone': input_phone, #add phone to the email content.
            }
            html_content = render_to_string('email-templates/email-contact-us.html', emailContent)

            # this is a quick fix, because for whatever reason, the "required" tag on the html page is not working.
            if len(input_first_name) != 0 and len(input_last_name) != 0 and "@" in input_email and len(input_message) != 0:
                try:
                    # send mail to company's email
                    mail = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [settings.DEFAULT_FROM_EMAIL])
                    mail.attach_alternative(html_content, "text/html")
                    mail.send()

                    messages.success(request, mark_safe('<strong>Message sent!</strong> Thank you for contacting Sisu VR, we will reply to you shortly!'))
                    
                    if is_ajax:
                        return JsonResponse({"response": "success", "message": "Message sent successfully!"})
                    
                    return redirect('/contact')

                except:
                    messages.error(request, mark_safe('<strong>Error occurred.</strong> Message could not be sent due to an error. </br>If this error persists please email <strong>hello@sisuvr.com</strong> directly. Thank you!'))
                    return redirect('/contact')

            else:
                messages.error(request, mark_safe('<strong>Error occurred.</strong> lease make sure you filled out all required fields. </br>If this error persists please email <strong>hello@sisuvr.com</strong> directly. Thank you!'))
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
                    PlaySession.objects.create(employer=employer.employer_id, player=newPlayer, module_id=module.module_id, score=0, success=False)

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
                'modules_completed': len(completed_modules)
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
    colorDict = {"hostile": 'rgba(196, 106, 108, 0.75)',
                 "passive": 'rgba(204, 155, 63, 0.75)', "confident": 'rgba(120, 158, 93, 0.75)'}

    return colorDict[behavior]


def portal_ethical_report(request, pk):
    if request.user.is_authenticated:

        player = Player.objects.get(user=request.user)
        play_sessions = PlaySession.objects.filter(player=str(player)).order_by('module_id')

        has_completed_all_mandatory, mandatory_modules_list = check_mandatory_completion(player, play_sessions)

        if not has_completed_all_mandatory:
            return render(request, 'portal/ethical-report.html', {"completedTraining": False})


        # supervisor can view aggregated report
        if player.supervisor and pk == "team_report":
            # filter team and aggregate data
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

            }

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

    # Hard-coded press artciles
    press_post_list = [
        {
            'p_title': 'This anti-sexual harassment training is designed to feel real: Is that a good thing?',
            'p_url': 'https://www.hr-brew.com/stories/2022/04/14/this-anti-sexual-harassment-training-is-designed-to-feel-real-is-that-a-good-thing',
            'p_photo': 'public/assets/img/press/press1.png', 
            'p_summary': 'VR companies want to heighten the “emotional stakes” of sexual harassment training.'
        },
        {
            'p_title': 'Your next sexual harassment training could be in virtual reality',
            'p_url': 'https://www.washingtonpost.com/technology/2022/04/19/virtual-reality-sexual-harassment-training/',
            'p_photo': 'public/assets/img/press/press2.png', 
            'p_summary': 'Some say the technology is game-changing. Others worry it could trigger survivors and do little to change bad behavior.'
        },
        {
            'p_title': 'Belästigung am Arbeitsplatz: Virtual-Reality-Brillen vermitteln, wie sich die junge Kollegin fühlt',
            'p_url': 'https://www.nzz.ch/technologie/belaestigung-am-arbeitsplatz-ploetzlich-schluepft-man-selbst-in-die-haut-der-jungen-kollegin-ld.1694782',
            'p_photo': 'public/assets/img/press/press3.png', 
            'p_summary': 'Mit ihrer Technologie wollen amerikanische Startups bei Mitarbeiterschulungen eindrücklicher vermitteln, was Belästigung, Diskriminierung und Rassismus bei den Betroffenen auslösen – und wie man richtig darauf reagiert.'
        },
        {
            'p_title': 'Workplace Conduct Training Through a Virtual Reality Lens',
            'p_url': 'https://iovine-young.usc.edu/the-pulse/virtual-reality-workplace-conduct-training-sisu',
            'p_photo': 'public/assets/img/press/press4.png', 
            'p_summary': "Sisu VR's Empower Now uses immersive VR to tackle workplace harassment by letting users experience real scenarios from different perspectives—building empathy and promoting meaningful change."
        },
        {
            'p_title': 'Inspirational Women 2023: Jocelyn Tan',
            'p_url': 'https://www.latimes.com/b2b/business-visionaries/inspirational-women/jocelyn-tan',
            'p_photo': 'public/assets/img/press/press5.png', 
            'p_summary': 'Jocelyn Tan is the founder of Sisu VR, using immersive tech to promote empathy and inclusion in the workplace.'
        },
        {
            'p_title': 'Can VR better prepare employees for the worst?',
            'p_url': 'https://thehustle.co/news/can-vr-better-prepare-employees-for-the-worst',
            'p_photo': 'public/assets/img/press/press6.png', 
            'p_summary': 'No one gets an Apple Vision Pro or a Meta Quest 3 and thinks, “Let\’s do active shooter training or learn about harassment." But that\’s what Sisu VR offers — an immersive way for companies to train employees for a day they hope never comes.'
        },
        {
            'p_title': 'Few Shocks, Plenty Of AWE As Immersive Industry Ventures To LBC',
            'p_url': 'https://www.forbes.com/sites/dbloom/2024/06/25/few-shocks-plenty-of-awe-as-immersive-industry-ventures-to-lbc/',
            'p_photo': 'public/assets/img/press/press7.png', 
            'p_summary': 'AWE 2024 brought together over 6,000 attendees and 300+ exhibitors in Long Beach, spotlighting the resilience and innovation of the immersive tech industry despite recent challenges.'
        },
        {
            'p_title': 'AWE 2024 Auggie Awards Finalists',
            'p_url': 'https://www.awexr.com/blog/AWE-2024-Auggie-Awards-Finalists',
            'p_photo': 'public/assets/img/press/press8.png', 
            'p_summary': 'Sisu VR\’s "Empower Now" and "Active Shooter Preparedness" trainings were recognized among the world\’s top XR solutions at the Auggie Awards, the leading honors for AR/VR excellence.'
        },
        {
            'p_title': 'Navigating Workplace Toxicity: Jocelyn Tan Of Sisu VR On Strategies for a Healthier Work Environment',
            'p_url': 'https://medium.com/authority-magazine/navigating-workplace-toxicity-jocelyn-tan-of-sisu-vr-on-strategies-for-a-healthier-work-8aa762244a12',
            'p_photo': 'public/assets/img/press/press9.png', 
            'p_summary': 'Jocelyn Tan discusses how Sisu VR uses immersive training to combat workplace toxicity and promote empathy.'
        },
        {
            'p_title': 'Virtual Reality: A Game-Changer for Workplace Safety and Active Shooter Training',
            'p_url': 'https://trainingindustry.com/articles/learning-technologies/virtual-reality-a-game-changer-for-workplace-safety-and-active-shooter-training/',
            'p_photo': 'public/assets/img/press/press10.png', 
            'p_summary': 'Virtual reality is helping employees prepare for workplace emergencies with realistic, hands-on active shooter training.'
        },
        {
            'p_title': '4 Signs That You Could Be Bullying Career Coworkers Unknowingly',
            'p_url': 'https://www.forbes.com/sites/bryanrobinson/2024/10/03/4-signs-that-indicate-you-could-be-bullying-career-coworkers/',
            'p_photo': 'public/assets/img/press/press11.png', 
            'p_summary': 'Jocelyn Tan shares signs of unintentional workplace bullying, how to take accountability, and steps to improve behavior. She also offers advice for victims on addressing and documenting mistreatment.'
        }
    ]


    # Hard-coded medium articles
    medium_article_list = [
        {
            'title_m': 'The DEI Puzzle: Five Myths That Feed the Fire 🔥',
            'url_m': 'https://sisuvr.medium.com/the-dei-puzzle-five-myths-that-feed-the-fire-985e2bdbc031',
            'm_photo': 'public/assets/img/articles/article1.png', 
            'Summary_m': "It’s a movement that has transformed global organizations. The first year after the Black Lives Matter protests, an estimated 94% of the 300,000 jobs advertised by S&P 100 companies went to people of color. It has also been proven to impact the bottom line; a 2020 McKinsey and Company study concluded companies with gender diversity in their leadership were 25% more likely to report higher profits."
        },
        {
            'title_m': '10 Best Practices to Ensure Your Compliance Training Hits Different',
            'url_m': 'https://sisuvr.medium.com/10-best-practices-to-ensure-your-compliance-training-hits-different-881a81b6ba61',
            'p_photo': 'public/assets/img/articles/article2.png', 
            'Summary_m': "Compliance training exists for a very real purpose — to ensure employees are kept up-to-date on what’s important. Specifically, learning about what’s legal, how they can be kept safe, and how to safeguard organizational assets and interest."
        },
        {
            'title_m': 'A Closer Look: The Past, Present, and Future of Workplace Violence',
            'url_m': 'https://sisuvr.medium.com/a-closer-look-the-past-present-and-future-of-workplace-violence-968f22461718',
            'm_photo': 'public/assets/img/articles/article3.png', 
            'Summary_m': "Workplace violence affects employees and organizations worldwide. Specifically in North America, learning from past incidents and key trends is essential for creating safer work environments."
        },
        {
            'title_m': '4 Apple Vision Pro Workplace Apps You Need To Try',
            'url_m': 'https://sisuvr.medium.com/4-apple-vision-pro-workplace-apps-you-need-to-try-7f85b13f7579',
            'm_photo': 'public/assets/img/articles/article4.png', 
            'Summary_m': "The long-anticipated Apple Vision Pro officially released on February 2nd and is currently available in the United States. There are currently over 1 million apps that are compatible with the device, including apps claiming to foster greater better productivity and collaboration. In this article, we hone in on four standout workplace apps for Vision Pro."
        },
        {
            'title_m': 'Unlock the Power of Compliance: Navigating Recent Labor Law Changes',
            'url_m': 'https://sisuvr.medium.com/unlock-the-power-of-compliance-navigating-recent-labor-law-changes-75306a1ac690',
            'm_photo': 'public/assets/img/articles/article5.png', 
            'Summary_m': "In today’s dynamic business landscape, staying informed about evolving labor laws is vital. Our comprehensive guide provides valuable insights into recent and upcoming labor law changes, helping you navigate the complexities and ensure compliance."
        },
        {
            'title_m': 'How ChatGPT, AI, and VR are Reshaping the Future of Employee Training',
            'url_m': 'https://sisuvr.medium.com/how-chatgpt-and-ai-are-reshaping-the-future-of-vr-training-3ec39a47a267',
            'm_photo': 'public/assets/img/articles/article6.png',
            'Summary_m': "Imagine stepping into a world where you can learn, practice, and refine your professional skills in a highly dynamic environment. This is the promise of the metaverse, an immersive environment that leverages augmented reality, virtual reality (VR), and mixed reality technologies. When you combine the metaverse with artificial intelligence (AI), what do you get?"
        },
        {
            'title_m': '5 Ways Virtual Reality is Used in Workplace Training',
            'url_m': 'https://sisuvr.medium.com/5-examples-of-virtual-reality-used-in-workplace-training-3f62ab3da089',
            'm_photo': 'public/assets/img/articles/article7.png',
            'Summary_m': "Inrecent years, virtual reality (VR) has become more accessible, offering employers an exciting new way to train their staff. VR allows employers to provide immersive, engaging, and cost-effective training opportunities that can help employees develop new skills and stay up to date with industry best practices. In this article, we’ll look at five examples of how employers are using VR to train their staff."
        },
        {
            'title_m': '4 Ways to Maximize Employee Learning',
            'url_m': 'https://sisuvr.medium.com/4-ways-to-maximize-employee-learning-a7f5ac82647',
            'm_photo': 'public/assets/img/articles/article8.png',
            'Summary_m': "Previously, we compared traditional training (e.g., PC-based, live lectures) to immersive learning using virtual reality (VR) technology. Specifically, immersive solutions can offer organizations a wide range of benefits, from enhanced employee engagement to improved safety."
        },
        {
            'title_m': 'Workplace Safety 101: Responding to Threats, Accidents, and Hazards',
            'url_m': 'https://sisuvr.medium.com/workplace-safety-101-responding-to-threats-accidents-and-hazards-3ef85725b11a',
            'm_photo': 'public/assets/img/articles/article9.png',
            'Summary_m': "Active threats, accidents, and hazards can pose serious risks to employee safety. While incidents are almost inevitable, with the right knowledge employees can effectively mitigate these harms. In this article, we will explore the various types of workplace threats, accidents, and hazards, and discuss ways to prevent each via immersive training."
        },
        {
            'title_m': '4 Ways to Enrich Soft Skills Through Immersive Learning',
            'url_m': 'https://sisuvr.medium.com/4-ways-to-enrich-soft-skills-through-immersive-learning-477f260650e1',
            'm_photo': 'public/assets/img/articles/article10.png',
            'Summary_m': "Developing core skills, also known as soft skills, is essential for professionals to thrive in the workplace. But did you know 87% of companies worldwide have realized or anticipate a soft skills gap?"
        },
        {
            'title_m': 'My Thoughts On…',
            'url_m': 'https://sisuvr.medium.com/my-thoughts-on-5fa8222849e0',
            'm_photo': 'public/assets/img/articles/article11.png',
            'Summary_m': "…best practices for creating a diverse and inclusive workplace, which can help prevent harassment and discrimination."
        },
        {
            'title_m': 'Transforming Training: From the Classroom to VR',
            'url_m': 'https://sisuvr.medium.com/transforming-training-from-the-classroom-to-vr-6b8b78219967',
            'm_photo': 'public/assets/img/articles/article12.png',
            'Summary_m': "Employee training is paramount. However, each individual has a distinct learning style–for example, one may prefer consuming content by listening, and another may prefer reading. With this in mind, what are some ways to deliver training experiences that will cater to a variety of learners?"
        },
        {
            'title_m': 'Combating Workplace Discrimination: The Power of Diversity, Inclusion, and Empathy',
            'url_m': 'https://sisuvr.medium.com/combating-workplace-discrimination-the-power-of-diversity-inclusion-and-empathy-9458bfb6645d',
            'm_photo': 'public/assets/img/articles/article13.png',
            'Summary_m': "Did you know 3 in 5 employees have witnessed or experienced workplace discrimination? Discrimination is the unjust treatment of an individual or group based on protected characteristics (i.e., personal traits) by an organization, or authority figures within an organization. For example, discrimination is exhibited when a worker gets promoted due to their gender. Or when an employee gets fired due to her religion."
        },
        {
            'title_m': 'Protecting Your People: Standing Up to Workplace Bullying',
            'url_m': 'https://sisuvr.medium.com/protecting-your-people-standing-up-to-workplace-bullying-ca52408755de',
            'm_photo': 'public/assets/img/articles/article14.png',
            'Summary_m': "No one should have to experience a hostile work environment. Unfortunately, workplace bullying is a reality for many employees, affecting millions of workers."
        },
        {
            'title_m': 'Empowerment through Awareness: Sexual Harassment in the Workplace',
            'url_m': 'https://sisuvr.medium.com/empowerment-through-awareness-sexual-harassment-in-the-workplace-abb111d5806e',
            'm_photo': 'public/assets/img/articles/article15.png',
            'Summary_m': "Did you know sexual harassment is the most common form of workplace harassment? In our previous article, we discussed various types of inappropriate workplace behavior. Today, we will be focusing on sexual harassment (SH), which includes any unsolicited or inappropriate sexual behavior or advances."
        },
        {
            'title_m': 'Workplace Misconduct 101',
            'url_m': 'https://sisuvr.medium.com/workplace-misconduct-101-3a5383e08164',
            'm_photo': 'public/assets/img/articles/article16.png',
            'Summary_m': "Inappropriate workplace behavior includes discrimination, harassment, bullying, and retaliation. Among other consequences, misconduct creates a hostile work environment, negatively impacting mental health, stress levels, and job satisfaction."
        },
        {
            'title_m': 'I Want to Build a….Virtual Reality Training Program!',
            'url_m': 'https://sisuvr.medium.com/i-want-to-build-a-virtual-reality-training-program-2c3181401e6d',
            'm_photo': 'public/assets/img/articles/article17.png',
            'Summary_m': "Through immersive learning, businesses can open doors to highly engaging training experiences that can have long-lasting benefits on staff productivity and connectedness."
        },
        {
            'title_m': '5 Major Industries in the Metaverse',
            'url_m': 'https://sisuvr.medium.com/five-major-industries-in-the-metaverse-13b92249b774',
            'm_photo': 'public/assets/img/articles/article18.png',
            'Summary_m': "Businesses in virtually every industry are recognizing the potential benefits of extended reality, which includes virtual reality (VR)."
        },
        {
            'title_m': 'Saving Lives Through Active Shooter Preparation',
            'url_m': 'https://sisuvr.medium.com/saving-lives-through-active-shooter-preparation-ec4f6f2aff0f',
            'm_photo': 'public/assets/img/articles/article19.png',
            'Summary_m': 'According to the FBI, an active shooting is when “one or more individuals [are] actively engag[ing] in killing or attempting to kill people in a confined space or populated area.”'
        },
        {
            'title_m': 'Empower Your Workforce in 2023',
            'url_m': 'https://sisuvr.medium.com/empower-your-workforce-in-2023-1ac3a0477295',
            'm_photo': 'public/assets/img/articles/article20.png',
            'Summary_m': "As we begin 2023, we ponder how organizations are cultivating an empowered workforce. Many companies are turning to more robust learning and development programs to create more informed and engaged teams. How are companies reimagining the way training is executed, especially in a rapidly changing, working world?"
        },
        {
            'title_m': '6 Big Brands Using VR for Training',
            'url_m': 'https://sisuvr.medium.com/6-big-brands-using-vr-for-training-63384140ffb4',
            'm_photo': 'public/assets/img/articles/article21.png',
            'Summary_m': "Ascompanies demand more engaging training content and methods for increased learning retention, traditional workforce training ought to evolve."
        },
        {
            'title_m': 'How VR is Changing Workplace Safety Trainings',
            'url_m': 'https://sisuvr.medium.com/how-vr-is-changing-workplace-safety-trainings-d441c992adf9',
            'm_photo': 'public/assets/img/articles/article22.png',
            'Summary_m': "Feeling safe, comfortable, and confident in the workplace is necessary to create a productive and professional work environment. However, violations of employee privacy, consent, and comfort occur frequently as a result of gender, racial, and sexual harassment and discrimination."
        },
        {
            'title_m': 'Life’s greatest secret…',
            'url_m': 'https://sisuvr.medium.com/lifes-greatest-secret-3d287768adf9',
            'm_photo': 'public/assets/img/articles/article23.png',
            'Summary_m': "Can you believe it is almost the end of December? With a new year just around the corner, it is a good time to reflect on what we have accomplished, and what is next. For 2022, where do we want to go, and who do we want to become?"
        },
        {
            'title_m': 'Why You Need Empathy in the Workplace',
            'url_m': 'https://sisuvr.medium.com/why-you-need-empathy-in-the-workplace-85dfb7a2d8c1',
            'm_photo': 'public/assets/img/articles/article24.png',
            'Summary_m': '“You never really understand a person until you consider things from his point of view…until you climb into his skin and walk around in it.”'
        },
        {
            'title_m': 'Get The Most Out Of Training Your Employees!',
            'url_m': 'https://sisuvr.medium.com/how-to-get-the-most-out-of-training-your-employees-3562581f3aa1',
            'm_photo': 'public/assets/img/articles/article25.png',
            'Summary_m': "Bettering your business through efficient training. Do you have a subject area or skill set you wish to train your employees to be proficient in?"
        },
        {
            'title_m': 'New Sexual Harassment Prevention Training Guidelines For California Businesses In The New Year',
            'url_m': 'https://sisuvr.medium.com/new-sexual-harassment-prevention-training-guidelines-for-california-businesses-in-the-new-year-133be7ec3a3f',
            'm_photo': 'public/assets/img/articles/article26.png',
            'Summary_m': "Catalyzed by the “Me Too” movement in 2018, California Governor Gavin Newsom signed Senate Bill (SB) 1343 and SB 778 to update the requirement of how many employees a company must have before they provide anti-sexual harassment training."
        },
        {
            'title_m': 'Increase User Retention, Comprehension, and Empathy Using Virtual Reality Training',
            'url_m': 'https://sisuvr.medium.com/increase-user-retention-comprehension-and-empathy-using-virtual-reality-training-7099a470e1f1',
            'm_photo': 'public/assets/img/articles/article27.png',
            'Summary_m': "Since its inception, virtual reality (VR) has had its limits pushed to see what the next advancement could be made of the technology. From a storytelling tool to interactive games in VR, the opportunities are endless. Studies have shown training using VR technology has increased benefits compared to traditional training videos. Increased comprehension, increased empathy, and a more interactive experience keep users engaged."
        },
        {
            'title_m': 'SISU VR’s Empower Now Program Comes To Life On Your Desktop',
            'url_m': 'https://sisuvr.medium.com/sisu-vrs-empower-now-program-comes-to-life-on-your-screen-c6292cf7ab1b',
            'm_photo': 'public/assets/img/articles/article28.png',
            'Summary_m': "The Empower Now Program (ENP), once offered exclusively through Virtual Reality, is now available to experience right on your desktop! SISU VR’s goal is to empower professionals to bring their best selves to work everyday with the help of effective and engaging anti-harassment training through virtual reality."
        },
        {
            'title_m': 'The Future of Work Is Now: VR Productivity Apps To Try Out',
            'url_m': 'https://sisuvr.medium.com/the-future-of-work-is-now-vr-productivity-apps-to-try-out-3c894290df8e',
            'm_photo': 'public/assets/img/articles/article29.png',
            'Summary_m': "COVID-19 has accelerated our need to perform remote work. To assist individuals in this new climate, leading-edge technologies, such as virtual reality (VR), are being used as a means to increase collaboration and throughput. "
        }
    ]

    latest_press_article_list = PressArticle.objects.order_by('-pub_date')[:11]
    latest_medium_post_list = MediumPost.objects.order_by('-pub_date_m')[:11]
    latest_linked_in_post_list = LinkedinPost.objects.order_by('-pub_date')[:3]

    template = loader.get_template('blog/news.html')
    context = {
        # 'press_post_list': press_post_list,
        # 'medium_article_list': medium_article_list,

        'latest_press_article_list': latest_press_article_list,

        'latest_medium_post_list': latest_medium_post_list,

        'latest_linked_in_post_list': latest_linked_in_post_list
    }

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
