# 507170536 吳韋德 
# 507170524 張亞亭

#-*- coding : utf-8 -*-
# coding: utf-8

import pandas as pd
from ipywidgets import *
import json
import glob
import os
from google_trans_new import google_translator
from IPython.display import display
from IPython.display import clear_output as clear

csv_df = None # 使用全域變數紀錄讀取的資料，方便其他 functon 使用
category_mapping = {} # 紀錄影片類別的字典 { id:類別 }
country_mapping = dict(美國='US', 日本='JP', 加拿大='CA', 德國='DE', 法國='FR',
                       英國='GB', 印度='IN', 墨西哥='MX', 南韓='KR', 全部='ALL')
country_mapping_revert = {v: k for k, v in country_mapping.items()} # 反轉 country_mapping，查詢使用
result = None # 資料分析的結果，提供給產出報表用

# 讀取紀錄影片類別的 json 檔案，並將結構轉換成字典 { id:類別 } 方便後續使用
def loadJson():
    path = 'data/US_category_id.json'
    global category_mapping
    with open(path, 'r') as obj:
        json_data = json.load(obj)
        for item in json_data['items']:
            id = int(item['id'])
            if(id not in category_mapping):
                category_mapping[id] = item['snippet']['title']

# 根據給定的參數資料，顯示前 n 筆資料，輸入參數為 (篩選的欄位, 要顯示幾筆, 排序:遞增或遞減 )
def show_top_n(properties, top_n, sort):
    csv_df[properties] = csv_df[properties].astype(int) # 資料型態轉成數字
    show_columns = ['title', properties]
    if len(csv_df.index) > 100000:
        show_columns.append('country')
    global result
    result = csv_df.sort_values(properties, ascending = sort)[show_columns]
    new_columns = []
    columns_mapping = {'title':'標題','views':'觀看次數','likes':'喜歡','dislikes':'不喜歡','comment_count':'留言數','country':'國家'}
    for column in result.columns:
        new_column = columns_mapping[column]
        new_columns.append(new_column)
    result.columns = new_columns
    display(result.head(top_n))

# 根據 video_id 欄位，移除重複的影片
def remove_duplicates():
    csv_df.drop_duplicates(subset='video_id', keep='last', inplace=True) # 有重複資料選擇最後一筆，並且直接替換舊的資料
    total = len(csv_df.index)
    return total


# 讀取影片資料(.csv)，參數為 ( 要讀取的國家 )
def loadData(country):
    global csv_df
    if country=='ALL':
        all_country_data =[]
        path = os.getcwd() + '\\data' # 設定資料的資料夾路徑
        path = os.path.abspath(path)  # 讀取指定資料夾內所有的 csv 路徑
        csv_paths = glob.glob(os.path.join(path, '*.csv')) # 讀取指定資料夾內所有的 csv 路徑組成 list
        print('已從 data 資料夾中讀取影片資料，資料處理中...\n')
        # 使用 for in 讀取每個 csv，在使用 concat 方法將所有 dataframe 接起來
        for f in csv_paths:
            print('\t'+f)
             # 找出是哪個國家的資料 ---- start
            strs = f.split('\\')
            fileName = strs[len(strs)-1]
            country_code = fileName.replace('videos.csv','')
            country_name = country_mapping_revert[country_code]
             # 找出是哪個國家的資料 ---- end
                
            temp_csv_df = pd.read_csv(f, encoding = 'utf-8', sep=',', error_bad_lines=False) # 讀取 csv
            
            # 在原本的 dataframe 新增國家的欄位 ---- start
            count = len(temp_csv_df.index)
            country_names = [country_name] * count
            temp_csv_df['country'] = country_names
            # 在原本的 dataframe 新增國家的欄位 ---- end
            
            all_country_data.append(temp_csv_df)
        csv_df = pd.concat(all_country_data) # 將每個國家的 dataframe 資料組合起來
        print('========================================================================================================\n')
        total = len(csv_df.index) # 原始資料量
        print('\n讀取' + country_mapping_revert[country] +'的影片資料，資料數量： ' + format(total,','))
        print('\n========================================================================================================\n')
        new_total = remove_duplicates() # 移除重複的資料
        print('移除重複的資料，新的資料數量：' + format(new_total,','))
        print('\n========================================================================================================\n')
        interact(show_top_n, properties=dict(觀看次數='views', 喜歡='likes', 不喜歡='dislikes', 留言數='comment_count'),
         top_n=(1,20), sort=dict(遞增=False, 遞減=True)) # 建立一個下拉選單，可以選擇屬性、資料筆數、排序方式，最後過濾出資料
    else:
        path = 'data/' + country + 'videos.csv'
        # 因為有多個語系，要設定 encoding = utf-8；原始資料某幾列的資料欄位數不對，會無法讀取，因此增加 error_bad_lines 忽略錯誤欄位
        csv_df = pd.read_csv(path, encoding = 'utf-8', sep=',', error_bad_lines=False) # 讀取 csv
        print('========================================================================================================\n')
        total = len(csv_df.index) # 原始資料量
        print('讀取' + country_mapping_revert[country] +'的影片資料，資料數量： ' + format(total,','))
        print('\n========================================================================================================\n')
        new_total = remove_duplicates() # 移除重複的資料
        
        print('移除重複的資料，新的資料數量：' + format(new_total,','))
        print('\n========================================================================================================\n')
        # 集中程度計算：(原始資料量 - 去重複後資料量) / 原始資料量 * 100
        concentrated = round(((total - new_total) / total) * 100, 2)
        print('熱門影片集中程度：' + str(concentrated) + '%')
        print('\n========================================================================================================\n')
        interact(show_top_n, properties=dict(觀看次數='views', 喜歡='likes', 不喜歡='dislikes', 留言數='comment_count'),
         top_n=(1,20), sort=dict(遞增=False, 遞減=True)) # 建立一個下拉選單，可以選擇屬性、資料筆數、排序方式，最後過濾出資料

loadJson() # 讀取存放影片類別的檔案(.json)

interact(loadData, country=country_mapping) # 建立一個下拉選單，可以選擇國家，並讀取該國家的影片資料