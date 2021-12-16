from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from users.models import CustomUser, UserProfile
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework_api_key.permissions import HasAPIKey
from .serializers import PlayerSerializer, PlaySessionSerializer, EmployeeSerializer, EmployerSerializer, ModulesSerializer, EthicalFeedbackSerializer
from .models import Player, PlaySession, Employee, Employer, Modules, EthicalFeedback
from rest_framework.parsers import JSONParser 
from rest_framework import status

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    #if not 
    queryset = Player.objects.all().order_by('email')
    serializer_class = PlayerSerializer

class PlaySessionViewSet(viewsets.ModelViewSet):
    queryset = PlaySession.objects.all().order_by('date_taken')
    serializer_class = PlaySessionSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

class ModulesViewSet(viewsets.ModelViewSet):
    queryset = Modules.objects.all()
    serializer_class = ModulesSerializer

@csrf_exempt
@api_view(['GET', 'POST'])
def addEthicalData(request):
    if request.method == 'POST':
        inputData = JSONParser().parse(request)
        print("input------")
        print(inputData)
        user = CustomUser.objects.get(email=inputData["data"]["session"]["Email"]).pk
        module = inputData["data"]["session"]["Module"]
        # timestamp = inputData["data"]["session"]["Date"]
        for ethical in inputData["data"]["ethical"]:
            scene = ethical["Scene"]
            behavior_id = ethical["Action"]
            emotion = ethical["Emotion"]
            data = {'user': user, 'module_id': module, 'scene': scene, 'behavior_id' : behavior_id, 'emotion': emotion}
            ethical_serializer = EthicalFeedbackSerializer(data=data)
            if ethical_serializer.is_valid():
                ethical_serializer.save()
            else:
                return JsonResponse(ethical_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(user, safe=False, status=status.HTTP_201_CREATED) 
 


@api_view(['GET', 'POST'])
def addSession(request):
    #session = request.data
    #data = {'employee_email': request.POST.get('email'), 'module_id': request.POST.get('id'), 'score': request.POST.get('score'), 'success': request.POST.get('success'), 'time_taken': request.POST.get('time')}
    usr = CustomUser.objects.get(email=request.GET['email'])
    print(usr)
    player = Player.objects.get(user=usr)
    data = {'module_id': request.GET['id'], 'player': player, 'score': request.GET['score'], 'success': request.GET['success'], 'time_taken': request.GET['time'], 'employer': '0', 'training_type': "2D"}
    session_serializer = PlaySessionSerializer(data=data)
    if session_serializer.is_valid():
        print("Session valid")
        session_serializer.save()
        return JsonResponse({'Success': 'YES'})
    else:
        print("Session not valid")
        print(session_serializer.errors)
        session_serializer.save()
        return JsonResponse({'Success': 'NO'})
        #return HttpResponse("Failure")
    #return Response(session_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def addPlayer(request):
    permission_classes = [HasAPIKey]
    player = request.data
    player_serializer = PlayerSerializer(player)
    player_serializer.save()
    return Response(player_serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
def login(request):
    User = get_user_model()
    if request.method == 'GET':
        employee_user = request.GET['user']
        employee_password = request.GET['pass']
        print (employee_user)
        try:
            username = Player.objects.get(email=employee_user)
            print (username)
        except ObjectDoesNotExist:
            print ("No entry found")
        #print ("Username: ")
        #print (username.email)
        try:
            playerUser = User.objects.get(email=employee_user)
            print (playerUser.username)
        except ObjectDoesNotExist:
            print ("No user found")
        user = authenticate(username=playerUser.username, password=employee_password)
        #user = authenticate(username=username, password=employee_password)
        
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
        #employee_serializer = EmployeeSerializer(employee)
