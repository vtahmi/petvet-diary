from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.PetListView.as_view(), name='pet_list'),
    path('add/', views.PetCreateView.as_view(), name='pet_create'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('<int:pk>/edit/', views.PetUpdateView.as_view(), name='pet_update'),
    path('<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet_delete'),

    path('<int:pet_pk>/vaccination/add/', views.VaccinationCreateView.as_view(), name='vaccination_create'),
]
