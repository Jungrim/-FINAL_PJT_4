from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('basicSelect', views.basicSelect),
    path('trendSelect',views.trendSelect)
]