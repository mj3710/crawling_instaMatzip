from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True) # 작성되는 시간이 자동적으로 반영됨
    update_date = models.DateTimeField(auto_now=True) #

    def __str__(self):
        return f'[{self.id}]{self.subject}'

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']

    #admin에서 어떻게 보일지 수정 지정하지 않으면 서브젝트 어쩌구로뜸
    def __str__(self):
        return f'[{self.board.id}]{self.board.subject}{self.content}'