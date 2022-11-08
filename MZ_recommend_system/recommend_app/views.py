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

from accounts.models import myuser

import sys
# sys.path.append("C:/workspaces/FINAL_PJT_4_DS&DE/MZ_recommend_system/recommend_app/ML_modeling")

import recommend_app.ML_modeling.recommend_ML as RML
df = RML.preprocessing_df()

basic_df, first_kmeans, first_pca = RML.first_clustering(df)
first_category, second_category = RML.create_category(df)
user = [5,1,2,3,4,3,0,0,0,0,0,1,0,0,0,0,0,1,1,1]
user_df,select = RML.user_scaling(first_category, second_category, user,df)
weighted_user_df = RML.weighting(user_df, df, select, 'user')
user_scaled = [weighted_user_df.loc['user'].values]
user_group, user_include_df = RML.user_clustering(basic_df, df , user_scaled, first_pca, first_kmeans)
result_dong_list = RML.similarity(user_df, df.loc[user_include_df.index.values], "user",3)
print(user_include_df.loc[result_dong_list]['DONG'].values)

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
    fin_nums = myuser.objects
    return render(request, 'recommend_app/category_ranking.html', {'fin_nums': fin_nums})
