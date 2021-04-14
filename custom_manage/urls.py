from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from .views import StaffUploadTemplateView, StaffUploadConfirmTemplateView

app_name = 'custom_manage'

urlpatterns = [
    path('upload/<int:pk>/', StaffUploadTemplateView.as_view(), name='staff_upload'),
    path('upload/<int:pk>/confirm/', StaffUploadConfirmTemplateView.as_view(), name='staff_confirm'),
    path('upload/<int:pk>/done/', views.confirm_done, name='confirm_done'),
]
