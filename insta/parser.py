import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from collections import Counter
from bs4 import BeautifulSoup

import platform

from config.settings.base import STATIC_DIR, BASE_DIR
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import pandas as pd
import requests
import folium
from folium.plugins import MarkerCluster

def insta_crawling():
    driver = webdriver.Chrome(r'D:\mjkim\playdata\chromedriver.exe')
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(10)

    #사용자 이름과 비밀번호를 입력합니다.
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    username.send_keys('username')
    password.send_keys('password')

    #로그인 버튼을 클릭합니다.
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    time.sleep(5)

    word = "제주도맛집"
    url = insta_searching(word) #url완성 메소드
    driver.get(url)
    time.sleep(7)

    # 첫 게시글 클릭
    select_first(driver)
    time.sleep(3)

    results = []
    target = 10
    for i in range(target):
        try:
            data = get_content(driver)
            results.append(data)
            move_next(driver)
        except:
            time.sleep(2)
            move_next(driver)
    return results


def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" + word
    return url


def select_first(driver):
    first = driver.find_element(By.CLASS_NAME, '_aagu')
    first.click()
    time.sleep(3)


def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    #     본문내용
    try:
        content = soup.select('div._a9zs > h1')[0].text
    except:
        content = ' '
    # 태그
    tags = re.findall(r'#[^\s#,\<]+', content)
    # 날짜정보
    date = soup.select('time._aaqe')[0]['datetime'][:10]
    # 좋아요 수
    try:
        like = soup.select('div._ae2s._ae3v._ae3w > section._ae5m._ae5n._ae5o > div > div > span > a > span > span')[0].text
    except:
        like = 0
    # 장소정보
    try:
        place = soup.select('div._aaqm')[0].text
    except:
        place = ''
    
    data = [content, date, like, place, tags]
    return data


def move_next(driver):
    right = driver.find_element(By.CLASS_NAME, '_aaqg')
    right.click()
    time.sleep(3)


def makeWordCloud(tags_total):
    #폰트 설정
    if platform.system() == 'Windows':   #윈도우의 경우
        font_path = "c:/Windows/Fonts/malgun.ttf"
    elif platform.system() == "Darwin":   #Mac 의 경우
        font_path = "/Users/$USER/Library/Fonts/AppleGothic.ttf"
    
    #이미지 경로 지정_import
    pic_info = STATIC_DIR / 'images/wordcloud1.png'

    #광고 걸러내기
    STOPWORDS = ['', '#일상','#맞팔','#먹팔맞팔','#울산맛집','#ootd','#fff', '#먹스타','#먹스타맞팔','#좋반','#소통','#제주포토존'
            ,'#먹방','#먹팔','#좋아요','#제주펜션','#데일리','#제주숙소','#팔로우', '#강남맛집','#홍대맛집','#부산맛집'
            ,'#부산역맛집','#영등포맛집','#해운대맛집','#부산대맛집','#광안리맛집','#전포동맛집','#동래맛집','#경성대맛집','#부평맛집','#김해맛집','#남포동맛집'
            ,'#부경대맛집','#전포카페거리','#가평맛집','#동탄맛집','#괴정맛집','#장유맛집','#사상맛집','#서면맛집','#초량맛집','#먹스타그램','#제주맘'
            ]

    tag_total_selected = []
    for tag in tags_total:
        if tag not in STOPWORDS:
            tag_total_selected.append(tag)

    tag_counts_selected = Counter(tag_total_selected)
    tag_counts_selected.most_common(50)

    #wordcloud 정의
    # 워드 클라우드 만들기
    wordcloud=WordCloud(font_path= font_path,	
                        background_color="white",
                        max_words=100,		
                        relative_scaling= 0.3, 	
                        width = 800,		
                        height = 400		
                    ).generate_from_frequencies(tag_counts_selected)

    # 막대 차트 그리기
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig(pic_info)


#받은 정보로 같은 항목이 몇번 언급됐는지 카운트했음
def makeMap(places_df):
    places_counts = places_df.value_counts()
    df_location_counts = pd.DataFrame(places_counts)
    locations = list(df_location_counts.index)
    locations_inform = []
    for location in locations:
        try:
            data = find_places(location)
            locations_inform.append(data)
            time.sleep(1)
        except:
            pass
    locations_inform_df = pd.DataFrame(locations_inform)
    locations_inform_df.columns = ['name_official', '경도','위도','인스타위치명']
    location_data = pd.merge(locations_inform_df, df_location_counts, how='inner', left_on='name_official', right_index=True)
    print(location_data)
    location_data = location_data.pivot_table(index=['name_official','경도','위도'], values='count', aggfunc='sum')
    location_data = location_data.reset_index()

    Mt_Hanla = [33.362500, 126.533694]
    map_jeju = folium.Map(location=Mt_Hanla, zoom_start=11)

    locations = []
    names = []
    for i in range(len(location_data)):
        data = location_data.iloc[i]
        locations.append((float(data['위도']), float(data['경도'])))
        names.append(data['name_official'])

    icon_create_function = """\
            function(cluster){
                return L.divIcon({
                    html:'<b>' + cluster.getChildCount() + '</b>',
                    className: 'marker-cluster marker-cluster-large',
                    iconsize: new L.Point(30,30)
                });
            }
    """
    marker_cluster = MarkerCluster(
        locations = locations, 
        popups = names,
        name = 'Jeju',
        overlay = True,
        control = True,
        icon_create_function = icon_create_function
    )

    marker_cluster.add_to(map_jeju)
    folium.LayerControl().add_to(map_jeju)

    map_jeju.save(BASE_DIR/'templates/map.html')

def find_places(searching):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
    headers = {
        "Authorization": "KakaoAK 7dfa31b3ddc8ac8f3d61254ba5bdec52"
    } 
    places = requests.get(url, headers = headers).json()['documents']
    place = places[0]

    name = place['place_name']
    x = place['x']
    y = place['y']
    # phone = place['phone']
    data = [name, x, y, searching]
    return data