from django.shortcuts import render
from django.http import JsonResponse
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os

from recommend_app.models import DongCnt


# from ML_modeling import recommend_ML

def index(request):
    return render(request, 'recommend_app/index.html')

def basicSelect(request):
    return render(request, 'recommend_app/prototype1.html')

def protoSubmit(request):
    # print(request)
    # print("****************************",os.getcwd())
    # user_input = []
    # user_input.append(request.POST['t'])
    # user_input.append(request.POST['sa'])
    # # user_input.append(request.POST['p'])
    # user_input.append(request.POST['c'])
    # user_input.append(request.POST['me'])
    # user_input.append(request.POST['st'])
    # user_input.append(request.POST['baby'])
    # user_input.append(request.POST['star'])
    # user_input.append(request.POST['ex'])
    # user_input.append(request.POST['sound'])
    # user_input.append(request.POST['mac'])
    # user_input.append(request.POST['le'])
    # user_input.append(request.POST['he'])
    # user_input.append(request.POST['gol'])
    # user_input.append(request.POST['car'])
    # user_input.append(request.POST['dog'])
    #
    # user_input = list(map(int, user_input))
    # cluster_df, user_df = user_predict_cluster(user_input, 'userID')
    # rc_seoul, rc_list = recommand_area(cluster_df, user_df, "userID")
    # c = cluster_df.loc[rc_list]['DONG'].values
    content = {"content" : "test"}
    return render(request, 'recommend_app/prototype2.html', content)

def categoryRanking(request):
    dong_cnt = DongCnt.objects
    return render(request, 'recommend_app/category_ranking.html', {'dong_cnt': dong_cnt})
