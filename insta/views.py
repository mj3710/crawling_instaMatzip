from django.shortcuts import render, redirect
from .parser import *
from .models import Insta
import pandas as pd

# Create your views here.
def index(request):  
    results = insta_crawling()
    for row in results:
        insta = Insta(content=row[0], date=row[1], like=row[2], place=row[3], tags=row[4])
        insta.save()
    return redirect('insta:wordcloud')

def wordcloud(request):
    #db에서 태그정보 가져와야함
    tags_all = Insta.objects.values('tags') #===select tags from Insta
     # 데이터프레임 형태로 바꿈
    tags_all_df = pd.DataFrame(tags_all)
    
    #글자 하나씩 뺴기
    tags_total = []

    for tags in tags_all_df['tags']:
        tags_list = tags[2:-2].split("', '")    
        for tag in tags_list:
            tags_total.append(tag)
    makeWordCloud(tags_total)
    return render(request, 'wordcloud.html')
    

def map(request):
    places = Insta.objects.exclude(place='').values('place')
    places_df = pd.DataFrame(places)
    makeMap(places_df)
    return render(request, 'map.html')

    #위치정보에서 place 가져와서 위도 경도를 따옴
    #카카오api 이용해서 위치정보 
    #db에 넣어둔 place 가져오자
    #근데 비어있는 값도 불러와서 그건 걸러서 가져오게 하고 싶어

    #장고가 리턴해준걸 판다스 데이터프레임에 담아
    #특정함수에 넘겨주자 거기서 작업할거야
    
    
