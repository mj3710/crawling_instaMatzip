from django import forms
from bbsnote.models import Board, Comment

# 클래스 안에 하위 클래스 작성 

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['subject', 'content']
        # widgets = {
        #     'subject' : forms.TextInput(attrs={'class':'form-control'}),
        #     'content' : forms.Textarea(attrs={'class':'form-control', 'rows': 10})
        # }
        # labels = {
        #     'subject' : '제목',
        #     'content' : '내용',
        # }
        
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글내용'
        }