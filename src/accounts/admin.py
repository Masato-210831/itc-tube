from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from .forms import CustomAdminChangeForm


class UserAdmin(BaseUserAdmin):
  form = CustomAdminChangeForm
  # 一覧ページ
  list_display = (
        "email",
        "active",
        "staff",
        "admin",
    )
  list_filter = (
    "admin",
    "active",
    )
  ordering = ("email",)
  filter_horizontal = ()
  
  #検索するフィールド
  search_fields = ('email',)
  
  
  #新規登録用
  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
  
  
  #編集用
  fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('プロフィール', {'fields': (
            'username',
            'department',
            'phone_number',
            'gender',
            'birthday',
        )}),
        ('権限', {'fields': ('staff','admin',)}),
    )
  
admin.site.register(User, UserAdmin)

#各Userページと統合したのでコメントアウト
# admin.site.register(Profile)