from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('pet/<int:pet_pk>/comment/add/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
