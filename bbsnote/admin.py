from django.contrib import admin
from .models import Board, Comment

# Register your models here.
#admin.site.register(Board)

# 검색기능 제공
class BoardAdmin(admin.ModelAdmin):
    # search_fields = ['subject']
    search_fields = ['subject', 'content']

admin.site.register(Board, BoardAdmin)

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']
admin.site.register(Comment, CommentAdmin)