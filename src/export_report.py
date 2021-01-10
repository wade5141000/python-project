# 507170536 吳韋德 
# 507170524 張亞亭

global result
report_type = 'Excel' # 導出的報表類別，預設是 Excel

# 切換選單時執行這個方法，修改 report_type
def choice_type(change):
    global report_type
    report_type = change.new

# 建立下拉選單並監聽 change 事件
option_list = ('Excel', 'Csv', 'Json')
dropdown = Dropdown(description="報表類型：", options=option_list)
dropdown.observe(choice_type, names='value')
display(dropdown)

# 點導出報表按鈕時執行這個方法，根據 report_type 產生對應的格式
def on_export(b):
    clear()
    display(dropdown)
    display(HBox([exportBtn]))
    display(HBox([previewBtn]))
    global report_type
    if report_type == 'Excel':
        print('導出 Excel 報表')
        result.to_excel('report.xls', sheet_name='sheet1')
    elif report_type == 'Csv':
        print('導出 Csv 報表')
        result.to_csv('report.csv')
    else:
        print('導出 Json 報表')
        with open('report.json', 'w', encoding='utf-8') as file:
            result.to_json(file, orient='index', force_ascii=False)
        
# 建立導出報表按鈕，並監聽 click 事件
exportBtn = Button(description="導出報表")
exportBtn.on_click(on_export)
display(HBox([exportBtn]))

# 點預覽資料按鈕時執行這個方法，顯示 result 的資料內容
def on_preview(b):
    clear()
    display(dropdown)
    display(HBox([exportBtn]))
    display(HBox([previewBtn]))
    display(result)

# 建立導出報表按鈕，並監聽 click 事件
previewBtn = Button(description="預覽資料")
previewBtn.on_click(on_preview)
display(HBox([previewBtn]))