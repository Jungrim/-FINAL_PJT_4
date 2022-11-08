from django.urls import path
from .import views

app_name = 'recommend_app'

urlpatterns = [
    path('', views.index),
    path('basicSelect', views.basicSelect, name='basicSelect'),
    path('protoSubmit',views.protoSubmit),
    path('categoryRanking',views.categoryRanking, name='categoryRanking'),

]