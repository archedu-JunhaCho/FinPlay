from django.urls import path
from . import views

urlpatterns = [
    path('loadRatedata/', views.loadRatedata),
    path('listAllrate/', views.listAllrate),
    path('detailrate/', views.detailrate),
]