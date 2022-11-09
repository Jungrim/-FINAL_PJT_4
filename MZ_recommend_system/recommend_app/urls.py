from django.urls import path
from . import views

app_name = 'recommend_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('basicSelect', views.basicSelect, name='basicSelect'),
    path('categoryRanking',views.categoryRanking, name='categoryRanking'),
]