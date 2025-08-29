# task_manager/accounts/urls.py

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # ユーザー登録
    path("signup/", views.signup_view, name="signup"),
    # ログイン
    path("login/", views.login_view, name="login"),
    # ログアウト
    path("logout/", views.logout_view, name="logout"),
]
