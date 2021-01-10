# 507170536 吳韋德 
# 507170524 張亞亭

authors = {} # 每個作者的影片數量
data_df2 = None

# 根據輸入值 n 可以決定要顯示的資料筆數
def show_result(top_n):
    global data_df2 # 使用全域變數
    total = len(data_df2.index)
    print('統計數量：' + str(total))
    sorted_result = sorted(authors.items(), key=lambda x:x[1], reverse=True) # 使用 lambda 函式，根據字典的 value 排序
    sorted_result_list = list(sorted_result)
    global result
    result = pd.DataFrame(sorted_result_list, columns=['作者', '數量'])
    display(result.head(top_n)) # 產生 dataframe 並顯示

# 根據國別統計熱門影片的作者排名
def findAuthors(country):
    global authors # 使用全域變數
    global data_df2 # 使用全域變數
    path = 'data/' + country + 'videos.csv'
    data_df = pd.read_csv(path, encoding = 'utf-8', sep=',', error_bad_lines=False)  # 讀取 csv 資料
    data_df2 = data_df.drop_duplicates(subset='video_id', keep='last') # 去除重複資料
    authors = {}
    for index, row in data_df2.iterrows(): # 迭代每一筆 dataframe
        author = row['channel_title']
        if author in authors: # 如果作者已經在字典裡，數量加 1
            authors[author] = authors[author]+1
        else:
            authors[author] = 1 # 如果作者沒有在字典裡，新增作者
    interact(show_result, top_n=(1,20)) # 提供數量選單，讓使用者決定顯示資料筆數
    
    
interact(findAuthors, country=dict(美國="US", 日本="JP", 加拿大='CA', 德國='DE', 法國='FR',
                                英國='GB', 印度='IN', 墨西哥='MX', 南韓='KR'))