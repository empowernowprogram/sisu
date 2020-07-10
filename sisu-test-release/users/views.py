# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm

# for user profile
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from mysite.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from .forms import PasswordResetRequestForm
from django.contrib import messages
from django.db.models.query_utils import Q

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import sendgrid
import os
from sendgrid.helpers.mail import *

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
def display_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=request.user.id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    context = {}
    context['f_name'] = user.first_name
    context['l_name'] = user.last_name
    context['photo'] = user_profile.photo
    
    return render(request, "blog/user_settings_profile.html", {
            "context": context,
        })

@login_required
def update_user(request, pk):
    f_name = request.GET.get('f_name')
    l_name = request.GET.get('l_name')
    user_photo = request.GET.get('profile_photo')
    custom_user = get_object_or_404(CustomUser, pk=request.user.id)
    
    if request.user.is_authenticated and request.user.id == custom_user.id:
        if request.method == "GET":        
           user_profile = get_object_or_404(UserProfile, user=custom_user)
                    
           custom_user.first_name = f_name
           custom_user.last_name = l_name
           user_profile.photo = user_photo
                   
           custom_user.save()
           user_profile.save()    
    return render(request, "blog/user_settings_profile.html")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
    
class DeleteUser(generic.DeleteView):
    template_name = 'blog/user_settings_profile_del.html'
    model = CustomUser
    
    def get_success_url(self):
        return reverse('contact_us') 

class ResetPasswordRequestView(FormView):
        template_name = "blog/forget_password.html"   
        success_url = reverse_lazy('password_reset_done')
        form_class = PasswordResetRequestForm

        @staticmethod
        def validate_email_address(email):
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False

        def post(self, request, *args, **kwargs):
       
            form = self.form_class(request.POST)
            if form.is_valid():
                data= form.cleaned_data["email"]
            if self.validate_email_address(data) is True:                 #uses the method written above
                associated_users= CustomUser.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                            c = {
                                'email': user.email,
                                'domain': request.META['HTTP_HOST'],
                                'site_name': 'mysisu.co',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                                'user': user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                                }
                            subject_template_name='registration/password_reset_subject.txt' 
                            # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                            email_template_name='registration/password_reset_email.html'    
                            # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                            subject = loader.render_to_string(subject_template_name, c)
                            # Email subject *must not* contain newlines
                            subject = ''.join(subject.splitlines())
                            email = loader.render_to_string(email_template_name, c)
                            #send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                            
                            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
                            from_email = Email("sisu.contact.us@gmail.com")
                            to_email = Email(user.email)
                            content = Content("text/plain", email)
                            
                            mail = Mail(from_email, subject, to_email, content)
                            response = sg.client.mail.send.post(request_body=mail.get())
                    result = self.form_valid(form)
                    #messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
            
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)
 