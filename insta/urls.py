from django.urls import path
from . import views

app_name = 'insta'

urlpatterns = [
    path('', views.index, name='index'), #db저장 루트
    path('wordcloud/',views.wordcloud, name='wordcloud'), #워드클라우드 루트
    path('map/', views.map, name='map'),
]