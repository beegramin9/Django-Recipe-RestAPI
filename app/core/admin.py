from django.contrib import admin
# Register your models here.

# 쟝고 디폴트 user admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# core 폴더의 models.py
from core import models
# 파이썬의 string을 human readable text로 바꾼다.
from django.utils.translation import gettext as _

# Useradmin은 뭐야 대체
class UserAdmin(BaseUserAdmin):
    # id로 order
    ordering = ['id']
    # email, name을 보여줌
    list_display = ['email', 'name']
    # 딕셔너리가 아니라 튜플이다
    fieldsets = (
        # change, create page의 섹션을 정의
        # 섹션 타이틀, 필드 
        # 맨 첫줄은 title, 즉 여긴 title이 None
        (None, {'fields' : ('email','password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    # add Page에 추가할 fields
    # 요기에 username이 아니라 email로 바꾸면 ID 기본설정이
    # email로 바뀌는 것
    add_fieldsets = (
        # 맨 첫줄은 title
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1' ,'password2')
        }),
    )



# UserAdmin을 User 모델에 등록하면 쟝고 admin에 등록이 완료됨
""" 쟝고 admin이 User 모델의 change를 follow할 수 있게함 """
admin.site.register(models.User, UserAdmin)
# User 모델이 아니라 평범한 CRUD 기능 가진 모델이라 따로 파라미터 없음ㄴ
admin.site.register(models.Tag)

