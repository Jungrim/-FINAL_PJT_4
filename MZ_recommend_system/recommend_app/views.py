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
    # if request.method == 'POST':
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         # 넘어온 데이터 db에 저장
    #         form.save()
    #         # user_name, password1을 추출 해서
    #         user_name = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         # 로그인 진행
    #         user = authenticate(username=user_name, password=raw_password)
    #         login(request, user)
    #         return redirect('/')
    # else:
    #     form = UserForm()
    # return render(request, 'recommend_app/recommendation.html', {'form':form})
    return render(request, 'recommend_app/recommendation.html')

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
    dict_list = []
    cate_list = ['transportation', 'safety', 'noise_vibration_num', 'leisure_num', 'gym_num', 'golf_num', 'park_num', 'facilities', 'medical', 'starbucks_num', 'mc_num', 'vegan_cnt', 'coliving_num', 'education', 'parenting', 'kids_num', 'ani_hspt_num', 'safe_dlvr_num', 'car_shr_num', 'mz_pop_cnt']
    
    for cate in cate_list:
        cnt_list = []
        dong_list = []
        dong_cnt = DongCnt.objects.filter(std_day__exact='2022-11-08').values_list(cate, flat=True).order_by('-' + cate).all()
        for i in range(0, 3):
            cnt_list.append(dong_cnt[i])
        dong = DongCnt.objects.filter(std_day__exact='2022-11-08').values_list('dong', flat=True).order_by('-' + cate).all()
        for i in range(0, 3):
            dong_list.append(dong[i])
        dictionary = {'category':cate, 'dong':dong_list, 'cnt':cnt_list}
        dict_list.append(dictionary)
    print(dict_list)

    return render(request, 'recommend_app/category_ranking.html', {'ranking':dict_list})
