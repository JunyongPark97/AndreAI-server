from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),
    path('model-cut/', views.model_cut_try, name='try-model'),
    path('detail-cut/', views.detail_cut_try, name='try-detail'),
    path('select/', views.select, name='select'),
    path('success/', views.success, name='success'),
]