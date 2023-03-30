from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
#3/23 템플릿 생성하기 코드
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    # 3/27 입력인자
    page = request.GET.get('page', 1)
    #return HttpResponse("bbsnote에 오신 것을 환영합니다.")
    # 3.23_1
    #가져온 정보 담은 보드 리스트 조회
    board_list = Board.objects.order_by('-create_date')

    #3/27 페이징처리
    paginator = Paginator(board_list, 5)
    page_obj = paginator.get_page(page)
    # 딕셔너리로 담기 
    context = {'board_list': page_obj}
    # 인덱스에 정의한 리퀘스트 
    return render(request, 'bbsnote/board_list.html', context)
    #이제 템플릿 정의 하러갑시다 뷰 구현은 끝남
    
def detail(request, board_id):
    board = Board.objects.get(id=board_id)
    context = {'board': board}
    return render(request, 'bbsnote/board_detail.html', context)

#import 까먹지 말고 해주기 주의
@login_required(login_url='common:login')
def comment_create(request, board_id):
    if request.method =='POST':
        board = Board.objects.get(id=board_id)
        # comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
        # comment.save()

        # Board와 Comment가 foreignKey로 연결되어있는 종속관계의 경우에는 위의 두 문장을 이렇게 한 줄로 쓸 수도 있다
        board.comment_set.create(content=request.POST.get('content'),create_date=timezone.now(), author=request.user)
    return redirect('bbsnote:detail', board_id=board_id)

@login_required(login_url='common:login')
def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid(): #값이 있냐 없냐 반환, 값이 있다면 아래 실행
            #실행은 하되 db에 넣지말고(커밋) 기다려봐 == mysql너 오토커밋하지마
            board = form.save(commit=False)
            #현재시간 할당하고 저장해
            board.create_date = timezone.now()
            board.author = request.user
            board.save()

            return redirect('bbsnote:index')
        
    else:#POST로 요청이 오지 않으면~
        form = BoardForm() 

    return render(request, 'bbsnote/board_form.html', {'form':form})

@login_required(login_url='common:login')
def board_modify(request, board_id):
    board = get_object_or_404(Board, pk=board_id) # 오류가 나면 오류 대신 404가 나오도록 처리
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.save()
            return redirect('bbsnote:detail', board_id=board.id)
    else:
        form=BoardForm(instance=board)
    context={'form' : form}
    return render(request, 'bbsnote/board_form.html', context)

@login_required(login_url='common:login')
def board_delete(request, board_id):
    board=get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    board.delete()
    return redirect('bbsnote:index')

    
@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # 작성자가 아닌 경우 예외처리
    if request.user != comment.author:
        messages.error(request, "수정 권한이 없습니다!")
        # bbsnote의 detail에 board_id를 넘겨주는데, board_id가 현재 comment가 종속된 board의 id인 곳으로 가라
        return redirect('bbsnote:detail', board_id=comment.board.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.save()
            return redirect('bbsnote:detail', board_id=comment.board.id)
    else:
        form = CommentForm(instance=comment)
    context={'comment':comment, 'form':form}
    return render(request, 'bbsnote/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제 권한이 없습니다!")
        return redirect('bbsnote:detail', board_id=comment.board.id)
    comment.delete()
    return redirect('bbsnote:detail', board_id=comment.board.id)