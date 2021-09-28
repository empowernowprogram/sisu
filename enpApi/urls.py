from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'playsessions', views.PlaySessionViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'employers', views.EmployerViewSet)
router.register(r'modules', views.ModulesViewSet)

urlpatterns = [
    path('api', include(router.urls)),
    path('employees/', views.login),
    path('addSession/', views.addSession),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('addEthicalData/', views.addEthicalData),
]
