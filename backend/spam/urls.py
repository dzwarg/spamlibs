from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('seed/<int:pk>/', views.index, name='seed'), # Placeholder
    path('list/<int:page>/', views.index, name='list'), # Placeholder
]