from django import template
register = template.Library()

# デコレータ
@register.filter
#デコレートする関数
def user_display(user):
  user_display = 'ゲスト'
  if user.is_authenticated:
    user_display = user.email
  return user_display