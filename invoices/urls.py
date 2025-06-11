from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_invoice, name='create_invoice'),
    path('success/', views.success, name='success'),
]
