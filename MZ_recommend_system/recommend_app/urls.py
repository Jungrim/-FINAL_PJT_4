from django.urls import path
from . import views

app_name = 'recommend_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('basicSelect', views.basicSelect, name='basicSelect'),
    path('protoSubmit',views.protoSubmit),
    path('result',views.result, name='result'),
    path('similar',views.similar, name='similar')
]