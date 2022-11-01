import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings

def minmax_norm(df):
    empty_df = pd.DataFrame()
    for c in df.columns:
        temp_df = (df[c] - df[c].min()) / ( df[c].max() - df[c].min())
        empty_df = pd.concat([empty_df, temp_df],axis=1)

    return empty_df

def data_preprocessing():

    tmp_df = pd.read_csv('data/행정동_기준_동별데이터_버스추가_1028.csv', index_col=0)
    tmp_df.set_index('DONG_CODE', inplace=True)

    # 교통
    tmp_df['교통'] = tmp_df['SUBWAY_NUM'] + tmp_df['BUS_CNT'] + tmp_df['BIKE_NUM']
    tmp_df = tmp_df.drop(['SUBWAY_NUM', 'BUS_CNT', 'BIKE_NUM'], axis=1)

    # 교육
    tmp_df['교육'] = tmp_df['MID_SCH_NUM'] + tmp_df['HIGH_SCH_NUM'] + tmp_df['ACADEMY_NUM'] + tmp_df['ELE_SCH_NUM']
    tmp_df = tmp_df.drop(['MID_SCH_NUM', 'HIGH_SCH_NUM', 'ACADEMY_NUM', 'ELE_SCH_NUM'], axis=1)

    # 육아
    tmp_df['육아'] = tmp_df['KIDS_NUM'] + tmp_df['CHILD_MED_NUM'] + tmp_df['KINDER_NUM']
    tmp_df = tmp_df.drop(['KIDS_NUM', 'CHILD_MED_NUM', 'KINDER_NUM'], axis=1)

    # 치안
    tmp_df['치안'] = tmp_df['SAFE_DLVR_NUM'] + tmp_df['POLICE_NUM'] + tmp_df['CCTV_NUM'] + tmp_df['FIRE_NUM']
    tmp_df = tmp_df.drop(['SAFE_DLVR_NUM', 'POLICE_NUM', 'CCTV_NUM', 'FIRE_NUM'], axis=1)


    # 건강
    tmp_df['건강'] = tmp_df['HOSPITAL_NUM'] + tmp_df['PHARM_NUM']
    tmp_df = tmp_df.drop(['HOSPITAL_NUM', 'PHARM_NUM'], axis=1)

    # 편의시설
    tmp_df['편의시설'] = tmp_df['DPTM_NUM'] + tmp_df['CON_NUM']
    tmp_df = tmp_df.drop(['DPTM_NUM', 'CON_NUM'], axis=1)

    tmp_df = tmp_df.drop(['CAFE_NUM', 'BUS_NUM'], axis=1)
    tmp_df = tmp_df[['GU', 'DONG', '교통', '치안', '편의시설', '건강', '교육', '육아',
                     'STARBUCKS_NUM', 'SPORT_NUM', 'NOISE_VIBRATION_NUM', 'MC_NUM',
                     'LEISURE_NUM', 'GYM_NUM', 'GOLF_NUM', 'CAR_SHR_NUM', 'ANI_HSPT_NUM']]
    tmp_df['NOISE_VIBRATION_NUM'] = np.where(tmp_df['NOISE_VIBRATION_NUM'] < 500, 4, (np.where(tmp_df['NOISE_VIBRATION_NUM'] <= 1000, 3, (np.where(tmp_df['NOISE_VIBRATION_NUM'] <= 1500, 2, 1)))))

    return tmp_df


def data_clustering():
    all_df = data_preprocessing()
    data = all_df.drop(['GU', 'DONG'], axis=1)
    data = minmax_norm(data)
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, random_state=0)
    kmeans.fit(data)

    basic_df = all_df.copy()
    basic_df['km_cluster'] = kmeans.labels_

    return basic_df, kmeans


def user_transform(user):  # min_Max Scaling 함수
    print("******",user)
    user_min = min(user)
    user_max = max(user)

    user_scaled = []
    for u in user:
        x = (u - user_min) / (user_max - user_min)
        user_scaled.append(x)
    return user_scaled


def user_predict_cluster(user_input, user_id):
    cluster_df, kmeans = data_clustering()
    col = cluster_df.columns[2:-1]
    user_df = pd.DataFrame(columns=col,index=[user_id])
    user_df.loc[user_id] = user_transform(user_input)
    cluster_user = kmeans.predict(user_df)
    user_df['km_cluster'] = cluster_user
    return cluster_df,user_df


def similarity(user_df, df, user_name, num): # 유저 데이터, 유사도 측정을 위한 데이터, 유저 이름, 원하는 순위
    con_data = pd.concat([user_df.loc[[user_name]],df])
    rc_sim = cosine_similarity(con_data,con_data)
    sim_matrix = pd.DataFrame(rc_sim,columns=con_data.index).loc[[0]].T
    rank = sim_matrix[0].sort_values(ascending=False) # 유사도 순서로 정렬
    ranking = rank[1:num+1].index.tolist() # 1~n 위 리스트
    return ranking


# 유저의 군집에 해당하는 지역 추출 함수
def recommand_area(df, user_df, user_name): # 지역 데이터, 유저 데이터, 유저 이름
    rc_area = user_df['km_cluster'].loc[user_name] # 해당 유저의 군집
    rc_seoul = df[df['km_cluster'] == rc_area] # 서울시 내 군집 지역 추출
    rc_sim_list = similarity(user_df.iloc[:,:-1],rc_seoul.iloc[:,2:-1],user_name,3)
    return rc_seoul, rc_sim_list
