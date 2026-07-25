from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('telecharger-pdf/', views.telecharger_pdf, name='telecharger_pdf'),
]