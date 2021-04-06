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
    # path('sell_intro/', views.sell_intro, name='sell_intro'),
    # path('success/', views.success, name='success'),
    # path('terms-of-use/', views.terms_of_use, name='terms-of-use'),
    # path('private-policy/', views.private_policy, name='private-policy'),
    #
    # path('register/', views.RegisterView.as_view(), name='register'),
]