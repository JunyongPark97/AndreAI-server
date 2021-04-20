from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'pictures'

urlpatterns = [
    path('try-model/', views.TryModelCutView.as_view(), name='try_model_cut'),
    path('try-detail/', views.TryDetailCutView.as_view(), name='try_detail_cut'),
    path('download/', views.DownloadView.as_view(), name='download'),
]