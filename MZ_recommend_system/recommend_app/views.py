from django.shortcuts import render, redirect
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

from recommend_app.models import DongCnt, InfraAdmin
from recommend_app.forms import WeightsForm
import sys
# sys.path.append("C:/workspaces/FINAL_PJT_4_DS&DE/MZ_recommend_system/recommend_app/ML_modeling")

import recommend_app.ML_modeling.recommend_ML as RML


def index(request):
    return render(request, 'recommend_app/index.html')

def basicSelect(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')
    if request.method == 'POST':
        form = WeightsForm(request.POST)
        if form.is_valid():
            # 넘어온 데이터 db에 저장
            form.save()
        req_dict = request.POST.dict()
        user = [int(i) for i in list(req_dict.values())[1:-1]]

        df = RML.preprocessing_df()
        basic_df, first_kmeans, first_pca = RML.first_clustering(df)
        first_category, second_category = RML.create_category(df)
        user_df, select = RML.user_scaling(first_category, second_category, user, df)
        weighted_user_df = RML.weighting(user_df, df, select, 'user')
        user_scaled = [weighted_user_df.loc['user'].values]
        user_group, user_include_df = RML.user_clustering(basic_df, df, user_scaled, first_pca, first_kmeans)
        result_dong_list = RML.similarity(user_df, df.loc[user_include_df.index.values], "user", 3)
        recommend_dong_list = user_include_df.loc[result_dong_list]['DONG'].values
        result = {"dong": recommend_dong_list, "weight_user": user}

        return render(request, 'recommend_app/recommend_result.html', {'result': result})
    else:
        form = WeightsForm()


    return render(request, 'recommend_app/recommendation.html', {'form':form})


def categoryRanking(request):
    dict_list = []
    cate_list = ['transportation', 'safety', 'noise_vibration_num', 'leisure_num', 'gym_num', 'golf_num', 'park_num', 'facilities', 'medical', 'starbucks_num', 'mc_num', 'vegan_cnt', 'coliving_num', 'education', 'parenting', 'kids_num', 'ani_hspt_num', 'safe_dlvr_num', 'car_shr_num', 'mz_pop_cnt']
    
    for cate in cate_list:
        cnt_list = []
        dong_list = []
        dong_cnt = DongCnt.objects.filter(std_day__exact='2022-11-08').values_list(cate, flat=True).order_by('-' + cate).all()
        dong = DongCnt.objects.filter(std_day__exact='2022-11-08').values_list('dong', flat=True).order_by('-' + cate).all()
        
        for i in range(0, 3):
            cnt_list.append(dong_cnt[i])
            dong_list.append(dong[i])
            
        dictionary = {'category':cate, 'dong':dong_list, 'cnt':cnt_list}
        dict_list.append(dictionary)
    print(dict_list)

    return render(request, 'recommend_app/category_ranking.html', {'ranking':dict_list})

def introduction(request):
    return render(request, 'recommend_app/introduction.html')

def dongDetail(request, dong_name):
    data = {"dong_name" : dong_name}
    print(dong_name)

    dict_list = []
    cate_list = ['transportation', 'safety', 'noise_vibration_num', 'leisure_num', 'gym_num', 'golf_num', 'park_num', 'facilities', 'medical', 'starbucks_num', 'mc_num', 'vegan_cnt', 'coliving_num', 'education', 'parenting', 'kids_num', 'ani_hspt_num', 'safe_dlvr_num', 'car_shr_num', 'mz_pop_cnt']
    
    for cate in cate_list:
        infra_name = InfraAdmin.objects.filter(std_day__exact='2022-10-27').filter(dong__exact=dong_name).filter(cate__exact=cate).values_list('name', flat=True).order_by('-name').all()
        infra_lat = InfraAdmin.objects.filter(std_day__exact='2022-10-27').filter(dong__exact=dong_name).filter(cate__exact=cate).values_list('lat', flat=True).order_by('-name').all()
        infra_lon = InfraAdmin.objects.filter(std_day__exact='2022-10-27').filter(dong__exact=dong_name).filter(cate__exact=cate).values_list('lon', flat=True).order_by('-name').all()
        name_list = []
        lat_list = []
        lon_list = []
        for i in range(len(infra_name)):
                name_list.append(infra_name[i])
                lat_list.append(float(infra_lat[i]))
                lon_list.append(float(infra_lon[i]))
        dictionary = {'category':cate, 'name':name_list, 'lat':lat_list, 'lon':lon_list}
        dict_list.append(dictionary)
    print(dict_list)
    return render(request, 'recommend_app/dong_detail.html', {'data' : data})
