# 507170536 吳韋德 
# 507170524 張亞亭

import warnings
warnings.filterwarnings('ignore') # 隱藏警告訊息
# 找出綜合評分最高的影片
def comprehensive(country):
    
    path = 'data/' + country + 'videos.csv'
    # 因為有多個語系，要設定 encoding = utf-8；原始資料某幾列的資料欄位數不對，會無法讀取，因此增加 error_bad_lines 忽略錯誤欄位
    data_df = pd.read_csv(path, encoding = 'utf-8', sep=',', error_bad_lines=False) # 讀取 csv
    new_data_df = data_df.drop_duplicates(subset='video_id', keep='last') # 有重複資料選擇最後一筆
    
    total_views = new_data_df['views'].sum() # 這個 dataframe 的總觀看數
    total_like = new_data_df['likes'].sum() # 這個 dataframe 的總喜歡數
    total_dislike = new_data_df['dislikes'].sum() # 這個 dataframe 的總不喜歡數
    total_comment = new_data_df['comment_count'].sum() # 這個 dataframe 的總評論數
    
    data_size = len(new_data_df.index)
    
    print('平均觀看次數：'+ format(round(total_views / data_size),','))
    print('平均喜歡人數：'+ format(round(total_like / data_size),','))
    print('平均不喜歡人數：'+ format(round(total_dislike / data_size),','))
    print('平均評論數：'+ format(round(total_comment / data_size),','))
    
    likes = total_like - total_dislike
    
    view_point = likes / total_views # 計算每個觀看次數值多少分
    like_point = 1 # 使用喜歡的數量當作基準值 1
    comment_point = likes / total_comment # 計算每個評論值多少分
    
    new_data_df['point'] = 0 # 初始化欄位 point
    
    # 計算每筆資料的分數
    def cal_point(row):
        point = 0
        point += (row['likes'] - row['dislikes']) * like_point # 計算喜歡分數
        point += row['views'] * view_point # 計算觀看分數
        point += row['comment_count'] * comment_point # 計算評論數分數
        row['point'] = point / 10000
        return row
    new_data_df = new_data_df.apply(cal_point, axis=1) # 針對每個欄位執行給定的方法
    global result
    result = new_data_df.sort_values('point', ascending = False)[['title','point','views','likes','dislikes','comment_count']]
    display(result.head(10))
    
interact(comprehensive, country=dict(美國="US", 日本="JP", 加拿大='CA', 德國='DE', 法國='FR',
                                英國='GB', 印度='IN', 墨西哥='MX', 南韓='KR'))
