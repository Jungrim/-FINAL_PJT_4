from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('basicSelect', views.basicSelect),
    path('protoSubmit',views.protoSubmit),
    path('categoryRanking',views.categoryRanking),

]