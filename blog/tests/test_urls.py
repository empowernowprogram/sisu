from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import index, about_us, contact, faq # for public pages
from blog.views import portal_home, portal_register, portal_edit_registration, portal_training_dl, portal_training_dl_trial, portal_employee_progress, portal_settings, post_program_survey, save_survey, portal_certificate, portal_edit, portal_remove, portal_change_password # for training pages
from blog.views import portal_login, portal_login_trial, portal_logout, portal_signup, key_redeem # for training portal authentication

class TestUrls(SimpleTestCase):
    
    """Public Site"""
    # Home
    def test_public_home_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    # FAQ 
    def test_public_faq_url_resolves(self):
        url = reverse('faq')
        self.assertEquals(resolve(url).func, faq)
        
    # About
    def test_public_about_us_url_resolves(self):
        url = reverse('about-us')
        self.assertEquals(resolve(url).func, about_us)

    # Contact Sales
    def test_public_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)
       
    """Training Portal"""
    # Authentication
    def test_training_auth_login(self):
        url = reverse('portal_login')
        self.assertEquals(resolve(url).func, portal_login)

    def test_training_auth_login_trial(self):
        url = reverse('portal_login_trial')
        self.assertEquals(resolve(url).func, portal_login_trial)
        
    def test_training_auth_logout(self):
        url = reverse('portal_logout')
        self.assertEquals(resolve(url).func, portal_logout)
        
    def test_training_auth_signup(self):
        url = reverse('portal_signup')
        self.assertEquals(resolve(url).func, portal_signup)
        
    def test_training_key_redeem(self):
        url = reverse('key_redeem')
        self.assertEquals(resolve(url).func, key_redeem)

    # Home
    def test_training_home_url_resolves(self):
        url = reverse('home_portal')
        self.assertEquals(resolve(url).func, portal_home)

    # Register
    def test_training_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, portal_register)

    # Edit registration
    def test_training_edit_registration_url_resolves(self):
        url = reverse('edit-registration')
        self.assertEquals(resolve(url).func, portal_edit_registration)

    # Downloads
    def test_training_downloads_url_resolves(self):
        url = reverse('downloads')
        self.assertEquals(resolve(url).func, portal_training_dl)

    # Downloads trial
    def test_training_downloads_trial_url_resolves(self):
        url = reverse('downloads_trial')
        self.assertEquals(resolve(url).func, portal_training_dl_trial)
    
    # Progress
    def test_training_progress_url_resolves(self):
        url = reverse('progress')
        self.assertEquals(resolve(url).func, portal_employee_progress)

    # Settings
    def test_training_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func, portal_settings)

    # Post program survey
    def test_training_survey_url_resolves(self):
        url = reverse('post_program_survey', args=['some-pk'])
        self.assertEquals(resolve(url).func, post_program_survey)

    # Post program survey (save)
    def test_training_save_survey_url_resolves(self):
        url = reverse('save_survey', args=['some-pk'])
        self.assertEquals(resolve(url).func, save_survey)

    # Certificate
    def test_training_certificate_url_resolves(self):
        url = reverse('certificate')
        self.assertEquals(resolve(url).func, portal_certificate)

    # Edit
    def test_training_edit_url_resolves(self):
        url = reverse('portal_edit')
        self.assertEquals(resolve(url).func, portal_edit)

    # Remove
    def test_training_remove_url_resolves(self):
        url = reverse('portal_remove')
        self.assertEquals(resolve(url).func, portal_remove)

    # Change password
    def test_training_password_url_resolves(self):
        url = reverse('portal_pwd')
        self.assertEquals(resolve(url).func, portal_change_password)