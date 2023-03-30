from django.urls import path
from . import views

#3/13_4?5?
app_name = 'bbsnote'

urlpatterns = [
    #콘피그 밑 유알엘을 먼저 만남 bbs노트 라는 주소가 있어? 그러면 넌 그 아래에 있는 유알엘을 참고하렴
    #아무것도 없는 경우에 뷰즈 인덱스를 실행해.
    path('', views.index, name='index'),
    #3_23_3
    path('<int:board_id>/', views.detail, name='detail'),  
    #이제 디테일 만들러 가자 만들고 url설정해도됨.
    #3.234?5?6? name 부여+아래
    path('comment/create/<int:board_id>/', views.comment_create,name='comment_create'),
    path('board/create/', views.board_create, name='board_create'),
    path('board/modify/<int:board_id>/', views.board_modify, name='board_modify'),
    path('board/delete/<int:board_id>/', views.board_delete, name='board_delete'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]