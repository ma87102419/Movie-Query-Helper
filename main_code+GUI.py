import googlemaps
import requests, json
"""
數據整理:
rank_list:排行榜前十名
movie_type_set:所有電影類型
movie_list:所有有在這8間電影院上映的電影＆基本資料
movie_set:所有有在這8間電影院上映的電影
theater_list = ['美麗華', '西門國賓', '絕色', '信義威秀', '百老匯', '秀泰', '京站威秀', '梅花']
theater_set = {'美麗華', '西門國賓', '絕色', '信義威秀', '百老匯', '秀泰', '京站威秀', '梅花'}
theater_dict:裝所有電影院的名稱、地址(Google map用)
movie_time_list:該部電影在這四天於八家電影院上映的場次
"""

def rank(line):  # 產出rank_list
    output_list = []
    line = line.strip()
    ranking = line.split(',')
    for i in range(10):
        if i == 9:
            ranking[i] = ranking[i][3:]
        else:
            ranking[i] = ranking[i][2:]
        output_list.append(ranking[i])
    return output_list

def import_movie(line):
	if len(line) == 1:
		pass
	else:
		line[1] = line[1].split()
		line[2] = line[2][5:11]
		line[3] = line[3][-10:]
		if line[4][:4] == 'IMDb':  # IMDb分數(如果沒有IMDb就不會放)
			line[4] = float(line[4][-3:])
		else:
			del line[4]
		return line

def check_time(movie_info):
	if len(movie_info[1]) == len(movie_info[2]) == len(movie_info[3]) == len(movie_info[4]) == 0:
		return False
	else:
		return True

def import_days(line):
	movie_time = []  # 一部電影的名稱 + 四天的播映場次
	movie_time.append(line[0][0])
	for d in range(1, 5):
		theater_time = [[], [], [], [], [], [], [], []]
		for t in range(len(line[d]) - 1):
			line[d][t] = line[d][t].split()
			for num in range(8):
				if line[d][t][0] == theater_list[num]:
					for j in range(1, len(line[d][t])):
						theater_time[num].append(str_to_time(line[d][t][j], d - 1))
		movie_time.append(theater_time)
	return(movie_time)

def str_to_time(string, d):  # 把字串14:50變時間2019-12-14 14:50:00
	string = date[d] + datetime.timedelta(hours = int(string[:2]), minutes = int(string[3:5]))
	# string = string.strftime('%H:%S')
	return string

import datetime
d1 = datetime.datetime.today()
d = d1.strftime('%Y-%m-%d')
d1 = datetime.datetime.strptime(d, '%Y-%m-%d')  # 化為0點0分
d2 = d1 + datetime.timedelta(days = 1)
d3 = d2 + datetime.timedelta(days = 1)
d4 = d3 + datetime.timedelta(days = 1)
date = [d1, d2, d3, d4]
date_list = []  # ['2019-12-15', '2019-12-16', '2019-12-17', '2019-12-18']
for i in range(4):
	date_list.append(date[i].strftime('%Y-%m-%d'))

movie_type_set = {'動畫', '動作', '冒險', '喜劇', '劇情', '愛情', '音樂/歌舞', '科幻', '犯罪', '懸疑/驚悚', '戰爭', '紀錄片', '溫馨/家庭', '恐怖', '歷史/傳記'}
theater_dict = {'台北市中山區敬業三路22號6樓': '美麗華', '台北市萬華區成都路88號': '西門國賓', '台北市萬華區漢中街52號10、11樓': '絕色', '台北市信義區松壽路18號': '信義威秀', '台北市文山區羅斯福路四段200號4樓': '百老匯', '台北市中正區羅斯福路四段136巷3號': '秀泰', '台北市大同區市民大道一段209號5樓': '京站威秀', '台北市和平東路3段63號2F': '梅花'}
theater_list = ['美麗華', '西門國賓', '絕色', '信義威秀', '百老匯', '秀泰', '京站威秀', '梅花']
theater_set = set(theater_list)
movie_list = []
movie_list2 = []
movie_time_list = []

with open('movie %s'% d, 'r') as f:
	line_cnt = 0
	for line in f:
		line_cnt += 1

line_cnt //= 5

with open('movie %s'% d, 'r') as f:
	line = f.readline()  # 第一行是前十名的資料
	rank_list = rank(line)

	for m in range(line_cnt):  # 跑50部電影
		movie_info = []
		for l in range(5):
			line = f.readline()
			line = line.strip()
			line = line.split(',')
			if l == 0:
				movie_info.append(import_movie(line))
			else:
				if len(line) == 1:
					movie_info.append([])
				else:
					movie_info.append(line)
		if check_time(movie_info) == True:
			movie_list.append(movie_info[0])
			movie_time_list.append(movie_info)

for i in range(len(movie_list)):
	movie_list2.append(movie_list[i][0])
movie_set = set(movie_list2)

for i in range(len(movie_time_list)):
	movie_time_list[i] = import_days(movie_time_list[i])

"""
rank_list完成
['野蠻遊戲：全面晉級', '冰雪奇緣2', '賽道狂人', '鋒迴路轉', '去年聖誕節', '82年生的金智英', '陽光普照', '特約經紀公司', '夕霧花園', ' 人間失格：太宰治與他的3個女人']

movie_set完成
{'鋒迴路轉', '野蠻遊戲：全面晉級', '去年聖誕節', '呆萌特務', '小丑', '魔鬼終結者：黑暗宿命', '布魯克林孤兒',
 '冰雪奇緣2', '82年生的金智英', 'Hello World', '人間失格：太宰治與他的3個女人', '決戰中途島',
 '為美好的世界獻上祝福！紅傳說', '賽道狂人', '紫羅蘭永恆花園外傳－永遠與自動手記人偶－', '特約經紀公司', '夕霧花園', '陽光普照'}

movie_list完成
['去年聖誕節', ['愛情', '喜劇'], '01時43分', '2019-12-06', 6.6]

movie_time_list完成
['小丑',
 [[], [], [datetime.datetime(2019, 12, 14, 20, 45)], [], [], [], [], []],
 [[], [], [datetime.datetime(2019, 12, 15, 20, 45)], [], [], [], [], []],
 [[], [], [], [], [], [], [], []],
 [[], [], [], [], [], [], [], []]]
"""
# ===========================以下是輸出部分===========================

"""
跑資料：印出前10名
搜尋電影：有三種方式
1.搜尋某部電影的相關資訊：片名，輸出片種、片長、上映日期、IMDb分數
2.搜尋某個類型的所有電影：輸入片種，輸出包含該片種的所有片名
3.多重篩選：輸入片名、電影院、日期、時間，輸出符合所有條件的選項
以上輸入到時候GUI用清單表示
"""

def search_movie(name):
	for i in range(len(movie_list)):
		if movie_list[i][0] == name:
			return movie_list[i]
			break

def search_type(name):
	output_list = []
	for i in range(len(movie_list)):
		if name in movie_list[i][1]:
			output_list.append(movie_list[i][0])
	return output_list

def movie_filter(line):
    search_movie_name = movie_combo.get()
    if line[0] == search_movie_name:
        return line



"""GUI"""
import tkinter as tk
from tkinter import ttk

win = tk.Tk()  # 建立主視窗



# 主視窗的名字
win.title('哈囉你要找電影嗎')

# 選擇視窗可否縮放
#win.resizable(False,False)

# 選擇要插入的背景圖片
fname = "background.png"
bg_image = tk.PhotoImage(file=fname)
w = bg_image.width()
h = bg_image.height()

# 視窗大小、背景圖片匯入
win.geometry("%dx%d+0+0" % (w, h))
cv = tk.Canvas(width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0,0, image=bg_image, anchor='nw')

# 搜尋時會用到的function
def movie_info_result():
    search_data = movie_time_list
    movie_info = tk.Tk()
    movie_info.title('哈囉這是你要的電影資訊')

    search_movie_name = movie_1_combo.get()
    output_list = search_movie(search_movie_name)
    info_out_list = []
    info_out_list.append(' 電影名稱 : {}'.format(output_list[0]))
    info_out_list.append(' 電影種類 : ')
    for i in range(len(output_list[1])):
        info_out_list[1] += output_list[1][i]
        info_out_list[1] += ' '
    info_out_list.append(' 電影長度 : {}'.format(output_list[2]))
    info_out_list.append(' 上映日期 : {}'.format(output_list[3]))
    try:
        info_out_list.append('IMDb分數: {}'.format(output_list[4]))
    except:
        pass

    info_out_str = '\n'
    for i in range(len(info_out_list)):
        info_out_str += info_out_list[i]
        info_out_str += '\n'

    movie_info_lb = tk.Label(movie_info, bg='white', fg='#323232', text=info_out_str, justify = 'left')
    movie_info_lb.config(font=('微軟正黑體', 20, 'bold'))  # 字型、大小、粗體等等調整
    movie_info_lb.pack(side = 'left')

def type_search_result():
    movie_type = tk.Tk()
    movie_type.config(background='#d5cdc0')
    movie_type.title('你可能會喜歡這些電影')

    search_movie_type = type_combo.get()
    output_list = search_type(search_movie_type)
    type_out_list = []
    if len(output_list) == 0:
        type_out_list.append('查無相關結果')
    else:
        type_out_list.append('{}電影 共有{}項搜尋結果:'.format(search_movie_type, len(output_list)))
        for i in range(len(output_list)):
            type_out_list.append(output_list[i])

    type_out_str = '\n'
    for i in range(len(type_out_list)):
        type_out_str += type_out_list[i]
        if i == 0:
            type_out_str += '\n\n'
        else:
            type_out_str += '\n'

    movie_type_lb = tk.Label(movie_type, bg='white', fg='#323232', text=type_out_str, justify='left')
    movie_type_lb.config(font=('微軟正黑體', 20))  # 字型、大小、粗體等等調整
    movie_type_lb.pack()

def timetable_search_result():
    import datetime
    d1 = datetime.datetime.today()
    d = d1.strftime('%Y-%m-%d')
    d1 = datetime.datetime.strptime(d, '%Y-%m-%d')  # 化為0點0分
    d2 = d1 + datetime.timedelta(days=1)
    d3 = d2 + datetime.timedelta(days=1)
    d4 = d3 + datetime.timedelta(days=1)
    date = [d1, d2, d3, d4]
    date_list = []  # ['2019-12-15', '2019-12-16', '2019-12-17', '2019-12-18']
    for i in range(4):
        date_list.append(date[i].strftime('%Y-%m-%d'))

    movie_type_set = {'動畫', '動作', '冒險', '喜劇', '劇情', '愛情', '音樂/歌舞', '科幻', '犯罪', '懸疑/驚悚', '戰爭', '紀錄片', '溫馨/家庭', '恐怖',
                      '歷史/傳記'}
    theater_dict = {'台北市中山區敬業三路22號6樓': '美麗華', '台北市萬華區成都路88號': '西門國賓', '台北市萬華區漢中街52號10、11樓': '絕色',
                    '台北市信義區松壽路18號': '信義威秀', '台北市文山區羅斯福路四段200號4樓': '百老匯', '台北市中正區羅斯福路四段136巷3號': '秀泰',
                    '台北市大同區市民大道一段209號5樓': '京站威秀', '台北市和平東路3段63號2F': '梅花'}
    theater_list = ['美麗華', '西門國賓', '絕色', '信義威秀', '百老匯', '秀泰', '京站威秀', '梅花']
    theater_set = set(theater_list)
    movie_list = []
    movie_list2 = []
    movie_time_list = []

    with open('movie %s'% d, 'r') as f:
        line_cnt = 0
        for line in f:
            line_cnt += 1
    line_cnt //= 5 

    with open('movie %s'% d, 'r') as f:
        line = f.readline()  # 第一行是前十名的資料
        rank_list = rank(line)

        for m in range(line_cnt):  # 跑50部電影
            movie_info = []
            for l in range(5):
                line = f.readline()
                line = line.strip()
                line = line.split(',')
                if l == 0:
                    movie_info.append(import_movie(line))
                else:
                    if len(line) == 1:
                        movie_info.append([])
                    else:
                        movie_info.append(line)
            if check_time(movie_info) == True:
                movie_list.append(movie_info[0])
                movie_time_list.append(movie_info)

    for i in range(len(movie_list)):
        movie_list2.append(movie_list[i][0])
    movie_set = set(movie_list2)

    for i in range(len(movie_time_list)):
        movie_time_list[i] = import_days(movie_time_list[i])
    
    search_data = movie_time_list
    search_movie_name = movie_combo.get()
    search_theater = theater_combo.get()
    search_date = date_combo.get()

    check_num = 1
    if search_movie_name != '':
        check_num *= 2
    if search_theater != '':
        check_num *= 3
    if search_date != '':
        check_num *= 5 

    # 篩選原理：被篩掉就把資料刪除
    origins = ['台北市']
    if search_theater != '' and address_entry.get() != '':
        movie_error = tk.Tk()
        movie_error.config(background='white')
        movie_error.title('錯誤訊息')
        movie_error_lb = tk.Label(movie_error, bg='white', fg='red', text='電影院及地址請擇一輸入！')
        movie_error_lb.config(font=('微軟正黑體', 20, 'bold'))  # 字型、大小、粗體等等調整
        movie_error_lb.pack()
    elif check_num == 1:
        movie_error = tk.Tk()
        movie_error.config(background='white')
        movie_error.title('錯誤訊息')
        movie_error_lb = tk.Label(movie_error, bg='white', fg='red', text='請輸入想要查詢的內容！')
        movie_error_lb.config(font=('微軟正黑體', 20, 'bold'))  # 字型、大小、粗體等等調整
        movie_error_lb.pack()
    elif search_date == '' and time_entry.get() != '':
        movie_error = tk.Tk()
        movie_error.config(background='white')
        movie_error.title('錯誤訊息')
        movie_error_lb = tk.Label(movie_error, bg='white', fg='red', text='請先輸入日期再輸入時間！')
        movie_error_lb.config(font=('微軟正黑體', 20, 'bold'))  # 字型、大小、粗體等等調整
        movie_error_lb.pack()
    else:
        movie_timetable = tk.Tk()
        movie_timetable.title('Timetable')
        sb = tk.Scrollbar(movie_timetable)
        sb.pack(side='right', fill='y')
        timetable = tk.Text(movie_timetable, yscrollcommand=sb.set, wrap='none', height=300, width=1000, font='微軟正黑體', fg='#323232')
        timetable.pack()        

    # 篩選原理：被篩掉就把資料刪除
    #origins = ['台北市']
    if search_movie_name == '':
        pass
    else:
        search_data = filter(movie_filter, search_data)
        search_data = list(search_data)

    gmap_check = True
    if search_theater == '':
        origins = [address_entry.get()]
        if origins == ['']:
            gmap_check = False
    else:
        for i in range(8):
            if theater_list[i] == search_theater:
                theater_id = i
                break
        for i in range(len(search_data)):
            for d in range(1, 5):
                for t in range(8):
                    if t != theater_id:
                        search_data[i][d][t] = []

    if search_date == '':
        pass
    else:
        search_time = time_entry.get()
        for d in range(4):
            if search_date != date_list[d]:
                for i in range(len(search_data)):
                    for t in range(8):
                        search_data[i][d + 1][t] = []
            else:
                search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d')
                if search_time == '':
                    pass
                else:
                    search_time = datetime.timedelta(hours = int(search_time[0:2]), minutes = int(search_time[3:5]))
                    search_date += search_time
                    for i in range(len(search_data)):
                        for t in range(8):
                            accept_time = []
                            for dt in range(len(search_data[i][d + 1][t])):
                                diff = search_date - search_data[i][d + 1][t][dt]
                                diff = abs(diff.total_seconds())

                                if diff < 7200:
                                    accept_time.append(search_data[i][d + 1][t][dt])
                            search_data[i][d + 1][t] = accept_time
    # 以下開始輸出
    search_output = []
    for i in range(len(search_data)):
        for d in range(1, 5):
            for t in range(8):
                if search_data[i][d][t] == []:
                    pass
                else:
                    for m in range(len(search_data[i][d][t])):
                        time = search_data[i][d][t][m].strftime('%Y-%m-%d %H:%M')
                        search_output.append([search_data[i][0], theater_list[t], time])

    # googlemap算距離
    final_output = []
    if gmap_check == True:
        # enter your api key here 
        api_key ='AIzaSyD8t3tzbH9b83tS6mzjqgbfp9cB7tMYKnU'
        # origins: test place
        # destinations : movie theater(numerous)
        destinations = ['台北市中山區敬業三路22號6樓', '台北市萬華區成都路88號', '台北市萬華區漢中街52號10、11樓', '台北市信義區松壽路18號',
                        '台北市文山區羅斯福路四段200號4樓', '台北市中正區羅斯福路四段136巷3號', '台北市大同區市民大道一段209號5樓', '台北市和平東路3段63號2F']
        gmap_dict = [{'dest': x} for x in destinations]

        # Requires API key
        gmaps = googlemaps.Client(key = api_key)

        # Requires cities name
        results = gmaps.distance_matrix('|'.join(origins), '|'.join(destinations))['rows'][0]['elements']

        for i,x in enumerate(results):
            gmap_dict[i]['duration'] = x['duration']['value']
        gmap_dict = sorted(gmap_dict, key = lambda x: x['duration'])   # 以開車車程(s)排序 秒數較少排前面



        # 將原本輸出依照電影院距離遠近排序

        Theater = 0
        for i in range(len(gmap_dict)):
            Theater = theater_dict[str(gmap_dict[i]['dest'])]
            for j in range(len(search_output)):
                if search_output[j][1] == Theater:
                    final_output.append(search_output[j])
    else:
        final_output = search_output

    for i in range(len(final_output)):
        final_output[i].append(final_output[i][2][-5:])
        final_output[i][2] = final_output[i][2][:10]
    
    def check_num_test(one, two, three, four, two_num, three_num):
        timetable_out_str = ''
        if i == 0:
            timetable_out_str += one
            timetable_out_str += '\n'
            if check_num < 6:
                timetable_out_str += '\n'
            timetable_out_str += two
            timetable_out_str += '\n'
            if 6 <= check_num < 15:
                timetable_out_str += '\n'
            timetable_out_str += three
            timetable_out_str += ' '
            timetable_out_str += four
        else:
            if final_output[i][two_num] == final_output[i - 1][two_num]:
                if final_output[i][three_num] == final_output[i - 1][three_num]:
                    timetable_out_str += ' '
                    timetable_out_str += four
                else:
                    timetable_out_str += '\n'
                    timetable_out_str += three
                    timetable_out_str += ' '
                    timetable_out_str += four
            else:
                timetable_out_str += '\n\n'
                timetable_out_str += two
                timetable_out_str += '\n'
                timetable_out_str += three
                timetable_out_str += ' '
                timetable_out_str += four
        return timetable_out_str

    output_str = '一共搜尋到{}項結果\n\n'.format(len(final_output))
    for i in range(len(final_output)):
        m = final_output[i][0]  # 電影名稱
        p = final_output[i][1]  # 電影院
        d = final_output[i][2]  # 電影日期
        t = final_output[i][3]  # 電影場次

        if check_num == 2 or check_num == 10 or check_num == 30:  # mdpt
            output_str += check_num_test(m, d, p, t, 2, 1)
        elif check_num == 3:  # pmdt  
            output_str += check_num_test(p, m, d, t, 0, 2)
        elif check_num == 5:  # dmpt
            output_str += check_num_test(d, m, p, t, 0, 1)
        elif check_num == 6:  # mpdt
            output_str += check_num_test(m, p, d, t, 1, 2)
        elif check_num == 15:  # pdmt
            output_str += check_num_test(p, d, m, t, 2, 0)

    try:
        timetable.insert(tk.END, output_str)
        sb.config(command=timetable.yview)
    except:
        pass

# 介面呈現上顯示
# 排行榜
for i in range(10):
    movie_name = rank_list[i]
    if i == 0:
        movie_lb = tk.Label(bg='white', fg='#323232', text='  No. '+str(i+1)+'    '+rank_list[i])
        movie_lb.config(font=('微軟正黑體', 16), anchor='nw')
        movie_lb.place(x=0, y=300, width=358, height=50)
    else:
        if i == 9:
            movie_lb = tk.Label(bg='white', fg='#323232', text='  No.'+str(i+1)+'  '+rank_list[i])
        else:
            movie_lb = tk.Label(bg='white', fg='#323232', text='  No. '+str(i+1)+'    '+rank_list[i])
        movie_lb.config(font=('微軟正黑體', 16), anchor='nw')
        movie_lb.place(x=0, y=300+40*i, width=358, height=50)

# 搜尋1選單
movie_1_combo = ttk.Combobox(cv, values=list(movie_set))
movie_1_combo.place(x=600, y=337, width=200, height=24)

# 搜尋2選單
type_combo = ttk.Combobox(cv, values=list(movie_type_set))
type_combo.place(x=600, y=585, width=200, height=24)

# 搜尋3選單
movie_combo = ttk.Combobox(cv, values=list(movie_set), height=20)
movie_combo.place(x=1066, y=338, width=200, height=24)

theater_combo = ttk.Combobox(cv, values=theater_list, height=20)
theater_combo.place(x=1066, y=387, width=200, height=24)

date_combo = ttk.Combobox(cv, values=date_list, height=20)
date_combo.place(x=1066, y=434, width=200, height=24)

address_entry = tk.Entry(cv, font='微軟正黑體')
address_entry.place(x=1066, y=484, width=200, height=24)

time_entry = tk.Entry(cv, font='微軟正黑體')
time_entry.place(x=1066, y=532, width=200, height=24)

# 搜尋1按鈕
movie_info_bt = tk.Button(cv, text='查詢', command=movie_info_result)
movie_info_bt.place(x=630, y=427)
# 搜尋2按鈕
movie_type_bt = tk.Button(cv, text='查詢', command=type_search_result)
movie_type_bt.place(x=630, y=680)
# 搜尋3按鈕
timetable_bt = tk.Button(cv, text='查詢', command=timetable_search_result)
timetable_bt.place(x=1100, y=680)

win.mainloop()