from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/', views.verify, name='verify'),
    path('verifyids/', views.verify_ids, name='verifyids'),
    path('verifyphone/', views.verify_phone, name='verifyphone'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='verify'),
    path('verifydocs/', views.verify_docs, name='verifydocs'),
    path('profile/', views.profile, name='verifyprofile'),
    
]
