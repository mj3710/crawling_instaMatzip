from django import template

register = template.Library()

#사용자 정의함수 장고에서 쓸 수 있게 하려고
# 가이드라인대로 모듈파서 정의한 것
@register.filter
def sub(value, arg):
    return value - arg