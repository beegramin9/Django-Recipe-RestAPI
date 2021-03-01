from django.urls import path
from user import views

# 어떤 app에서 url을 만들어서 가져오는지
# test 파일에서 reverse로 만든 app 이름과 같다
app_name = 'user'
urlpatterns = [
    # name에 주는 것은 test 파일의 reverse의 url과 매치되야 한다
    # user:create
    path('create/', views.CreateUserView.as_view(), name = 'create'),
    path('token/', views.CreateTokenView.as_view(), name = 'token'),
]