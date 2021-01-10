# 507170536 吳韋德 
# 507170524 張亞亭

categorys = {} # 每個類別的數量紀錄

# 根據類別 id 找出對應類別
def findCategoryById(id):
    global categorys
    global category_mapping
    title = category_mapping[id]
    if title in categorys: # 如果類別已經在字典裡，數量加 1
        categorys[title] = categorys[title]+1
    else: # 如果類別沒有在字典裡，新增類別
        categorys[title] = 1

# 根據國別統計熱門影片的類別偏好
def findCategorys(country):
    global categorys
    categorys = {}
    path = 'data/' + country + 'videos.csv'
    data_df = pd.read_csv(path, encoding = 'utf-8', sep=',', error_bad_lines=False) # 讀取 csv 資料
    data_df2 = data_df.drop_duplicates(subset='video_id', keep='last') # 去除重複資料
    for index, row in data_df2.iterrows():
        findCategoryById(row['category_id']) # 每一筆資料使用 findCategoryById 函式找出對應的類別
    print('統計影片數量：' + str(len(data_df2.index)))
    sorted_result = sorted(categorys.items(), key=lambda x:x[1], reverse=True) # 使用 lambda 函式，根據字典的 value 排序
    sorted_result_list = list(sorted_result)
    
    translator = google_translator() # 啟動 google 翻譯
    translate_data = []
    for cate in sorted_result_list:
        translate_text = translator.translate(cate[0], lang_src='en', lang_tgt='zh-tw') # 翻譯英文成繁體中文
        translate_data.append(translate_text)
    global result
    result = pd.DataFrame(sorted_result_list, columns=['影片類別', '數量']) # 轉換成 dataframe
    result['類別中文'] = translate_data # 新增 dataframe 欄位
    display(result) 

interact(findCategorys, country=dict(美國="US", 日本="JP", 加拿大='CA', 德國='DE', 法國='FR',
                                英國='GB', 印度='IN', 墨西哥='MX', 南韓='KR'))
