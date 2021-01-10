# 507170536 吳韋德 
# 507170524 張亞亭

import warnings
warnings.filterwarnings('ignore') # 隱藏警告訊息

global result

indexes = ['title', '標題', '影片類別', '作者'] # 圖的欄位
numbers = ['觀看次數','喜歡','不喜歡','留言數','point', '數量'] # 圖的資料
index = 0
df_to_draw = None

# 使用 while 加上例外處理，尋找要繪製的資料內，欄位的正確名字
while True:
    try:
        df_to_draw = result.set_index(indexes[index])
        break
    except KeyError:
        index += 1
    except:
        print('something wrong')
        break

df_to_draw = df_to_draw.head(10) # 取前 10 筆資料繪圖

# 根據不同的圖表類別，繪製圖表
def draw(kind):
    n_index = 0
    # 使用 while 加上例外處理，尋找要繪製的資料內，資料的正確名字
    while True:
        try:
            df_to_draw[numbers[n_index]].plot(kind=kind)
            break
        except KeyError:
            n_index += 1
        except:
            print('something wrong')
            break

interact(draw, kind=dict(柱狀圖="bar", 橫向柱狀圖="barh", 派餅圖="pie"))