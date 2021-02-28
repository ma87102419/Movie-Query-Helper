import time
import datetime
from selenium import webdriver
browser = webdriver.Chrome('/Users/ruby/Desktop/chromedriver')
website = "https://movies.yahoo.com.tw/movie_thisweek.html?page=0"
movie_list = []
movie_link = []
ranking_list = []
d = datetime.datetime.today()
for pages in range(2):
    website = website.replace(str(pages), str(pages+1))
    browser.get(website)
    browser.set_page_load_timeout(110)
    release_movie_time = browser.find_elements_by_class_name('release_movie_time')
    info_lst = browser.find_elements_by_class_name("gabtn")
    movie_info_link_website = "https://movies.yahoo.com.tw/movieinfo_main/"
    r_time = "上映日期"
    for i in range(len(release_movie_time)):
        release_movie_time_str = release_movie_time[i].text.split('：')
        release_movie_time_str[1] = release_movie_time_str[1].strip()
        release_movie_time_str[1] = datetime.datetime.strptime(release_movie_time_str[1], '%Y-%m-%d')
        diff = d - release_movie_time_str[1]
        if diff.days >= 0:
            a = browser.find_element_by_xpath('//*[@id="content_l"]/div[2]/ul/li['+str(i+1)+']/div[2]/div[1]/div[1]/a')
            movie_data_str = a.get_attribute("data-ga").strip("[]").replace("'", "")
            movie_data = movie_data_str.split(",")
            if movie_data[0] == "本週新片" and movie_data[2] not in movie_list:
                movie_list.append(movie_data[2])
                movie_link.append(a.get_attribute('href'))
        for info in info_lst:
            if movie_info_link_website in str(info.get_attribute("href")):
                movie_data_str = info.get_attribute("data-ga").strip("[]").replace("'", "")
                movie_data = movie_data_str.split(",")
                if pages == 0 and movie_data[1] == "電影排行榜_台北票房榜":
                    print(movie_data)
                    print(info.text)
                    if len(info.text) > 0:
                        for i in range(1, 10):
                            if str(i) == info.text[0]:
                                ranking_list.append(info.text)
d = d.strftime('%Y-%m-%d')
with open('movie %s' % d, 'a') as f:
    for i in range(10):
        if i == 9:
            f.write(ranking_list[i] + '\n')
        else:
            f.write(ranking_list[i] + ',')


website = "https://movies.yahoo.com.tw/movie_intheaters.html?page=0"
for pages in range(5):
    website = website.replace(str(pages), str(pages + 1))
    browser.get(website)
    browser.set_page_load_timeout(110)
    info_lst = browser.find_elements_by_class_name("gabtn")
    movie_info_link_website = "https://movies.yahoo.com.tw/movieinfo_main/"
    for info in info_lst:
        if movie_info_link_website in str(info.get_attribute("href")):
            movie_data_str = info.get_attribute("data-ga").strip("[]").replace("'", "")
            movie_data = movie_data_str.split(",")
        if movie_data[0] == "上映中" and movie_data[2] not in movie_list:
            movie_list.append(movie_data[2])
            movie_link.append(info.get_attribute("href"))
for l in movie_link:
    browser.get(l)  # 進到每個電影的網址
    browser.set_page_load_timeout(110)
    movie_name_Chinese = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/h1').text
    # movie_name_English = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/h3').text
    movie_type = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/div[2]').text.replace('\n', ' ')
    release_date = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/span[1]').text
    length = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/span[2]').text
    IMDb_score = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[2]/div/div/div[2]/span[4]').text
    # 用每個的xpath抓東西 然後用逗點隔開寫到檔案裡
    print(movie_name_Chinese + ',' + movie_type + ',' + length + ',' + release_date + ',' + IMDb_score)
    with open('movie %s' % d, 'a') as f:
        f.write(movie_name_Chinese + ',' + movie_type + ',' + length + ',' + release_date + ',' + IMDb_score + '\n')

    theater_id_list = [32, 37, 42, 45, 52, 53, 118, 126]
    theater_id_name_list = ['美麗華', '西門國賓', '絕色', '信義威秀', '百老匯', '秀泰', '京站威秀', '梅花']
    try:
        timetable = browser.find_element_by_xpath('//*[@id="content_l"]/div[1]/div[1]/ul/li[5]/a').get_attribute('href')
        browser.get(timetable)
        browser.set_page_load_timeout(110)
        time.sleep(5)
    except:
        print('no info')
        continue

    for i in range(4):
        try:
            browser.find_element_by_xpath('//*[@id="content_l"]/div/div/div[2]/div[1]/ul/li['+str(i+1)+']/label/h3').click()
            browser.set_page_load_timeout(110)
            time.sleep(5)
            no = 0
            for i in range(8):
                try:  # 找找看有沒有那八家
                    movie_time_list = browser.find_element_by_id('theater_id_' + str(theater_id_list[i])).text.split('\n')
                    movie_time = theater_id_name_list[i]  # 創一個電影院的字串
                    for t in movie_time_list:
                        if ':' in t:  # 把時間加到字串後面
                            movie_time += ' ' + t
                    print(movie_time, end=',')
                    with open('movie %s' % d, 'a') as f:  # 檔名設為movie加今天時間
                        f.write(movie_time + ',')  # 把時間寫進檔案裡
                except:
                    no += 1
            if no == 8:
                print('N', end='')
                with open('movie %s' % d, 'a') as f:
                    f.write('N')  # 那天那八間電影院都沒有
        except:
            print('no info', end='')
            with open('movie %s' % d, 'a') as f:
                f.write('no info')
        print()
        with open('movie %s' % d, 'a') as f:
            f.write('\n')
browser.quit()

