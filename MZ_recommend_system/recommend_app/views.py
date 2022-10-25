from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'recommend_app/index.html')

def basicSelect(request):
    return render(request, 'recommend_app/basicSelect.html')

def trendSelect(request):
    rating_traffic = request.POST['rate_1']
    rating_safety = request.POST['rate_2']
    rating_environment = request.POST['rate_3']
    rating_facility = request.POST['rate_4']
    rating_health = request.POST['rate_5']
    print(rating_traffic,rating_safety ,rating_environment, rating_facility, rating_health)
    return render(request, 'recommend_app/trendSelect.html')