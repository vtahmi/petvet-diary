from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pets', views.PetViewSet, basename='pet')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]