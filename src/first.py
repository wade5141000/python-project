import json

file = 'src/data/US_category_id.json'
with open(file, 'r') as obj:
    data = json.load(obj)

id=19

for x in data['items']:
    if(int(x['id']) == id):
        print(x['snippet']['title'])
    

# 轉換分析後寫出檔案

# 畫圖展示

# data frame 合併統計