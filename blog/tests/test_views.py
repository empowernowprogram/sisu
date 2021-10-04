from django.test import TestCase, Client
from django.urls import reverse
from enpApi.models import Player, PlaySession, Adjective, ComparisonRating, PostProgramSurvey, PostProgramSurveySupervisor, SelectedAdjective
from users.models import CustomUser
import json


class TestPostProgramSurveyViews(TestCase):

    def setUp(self):

        self.client = Client()

        # post program survey related urls
        self.get_survey_url = reverse('post_program_survey', args=['nonsupervisor'])
        self.get_survey_supervisor_url = reverse('post_program_survey', args=['supervisor'])

        self.post_survey_url = reverse('save_survey', args=['nonsupervisor'])
        self.post_survey_supervisor_url = reverse('save_survey', args=['supervisor'])

        # create user
        self.user = CustomUser.objects.create(username='testuser')
        self.user.set_password('12345') # hash '12345'
        self.user.save()

        # create user (supervisor)
        self.user_supervisor = CustomUser.objects.create(username='testuser_supervisor')
        self.user_supervisor.set_password('12345') # hash '12345'
        self.user_supervisor.save()

        # create player
        self.player = Player.objects.create(
            email='test@mail.com',
            employer=0,
            full_name='testName',
            user=self.user
        )

        # create player (supervisor)
        self.playerSuper = Player.objects.create(
            email='test_super@mail.com',
            employer=0,
            supervisor=True,
            full_name='testName_super',
            user=self.user_supervisor
        )

        # create adjectives and preference options
        Adjective.objects.create(
            adj_id=0,
            description='adj0'
        )
        Adjective.objects.create(
            adj_id=1,
            description='adj1'
        )
        ComparisonRating.objects.create(
            comparison_rating_id=0,
            description='test'
        )


    def test_nonsupervisor_survey_GET(self):

        # login user
        self.client.login(username='testuser', password='12345')

        # create play session
        PlaySession.objects.create(
            player=self.player,
            employer=0,
            module_id=1,
            score=100,
            success=True,
            time_taken=40
        )

        # case 1: if user tries to access survey for nonsupervisor
        response = self.client.get(self.get_survey_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/post-program-survey.html')

        # case 2: if user tries to access survey for supervisor
        response = self.client.get(self.get_survey_supervisor_url)

        self.assertRedirects(response, '/portal/home/')

        #case 3: if user had already completed survey
        PostProgramSurvey.objects.create(
            user=self.user,
            overall_rating=5
        )

        response = self.client.get(self.get_survey_url)

        self.assertRedirects(response, '/portal/certificate/')


    def test_supervisor_survey_GET(self):

        # login user
        self.client.login(username='testuser_supervisor', password='12345')

        # create play session
        PlaySession.objects.create(
            player=self.playerSuper,
            employer=0,
            module_id=1,
            score=100,
            success=True,
            time_taken=40
        )

        # case 1: if user tries to access survey for supervisor
        response = self.client.get(self.get_survey_supervisor_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/post-program-survey-supervisor.html')

        # case 2: if user tries to access survey for nonsupervisor
        response = self.client.get(self.get_survey_url)

        self.assertRedirects(response, '/portal/home/')

        #case 3: if user had already completed survey
        PostProgramSurveySupervisor.objects.create(
            user=self.user_supervisor
        )

        response = self.client.get(self.get_survey_supervisor_url)

        self.assertRedirects(response, '/portal/certificate/')


    def test_save_nonsupervisor_survey_POST(self):

        # login user
        self.client.login(username='testuser', password='12345')

        response = self.client.post(self.post_survey_url, {
            'user': self.user,
            'overallStars': 5
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(PostProgramSurvey.objects.get(user=self.user).overall_rating, 5)

        # if user tries to access survey for supervisor
        response = self.client.post(self.post_survey_supervisor_url, {
            'user': self.user,
            'overallStars': 5
        })

        self.assertRedirects(response, '/portal/home/')

    def test_save_supervisor_survey_POST(self):
        
        # login user
        self.client.login(username='testuser_supervisor', password='12345')

        response = self.client.post(self.post_survey_supervisor_url, {
            'user': self.user_supervisor,
            'preference': 0,
            'features': ('0','1')
        })

        self.assertEquals(response.status_code, 200)

        # check comparison_rating_id is stored correctly
        self.assertEquals(PostProgramSurveySupervisor.objects.get(user=self.user_supervisor).comparison_rating_id.comparison_rating_id, 0)

        # check selected adjectives are stored correctly
        self.assertEquals(len(SelectedAdjective.objects.get(user=self.user_supervisor).adj_id.all()), 2)

