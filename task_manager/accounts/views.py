# task_manager/accounts/views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm


def signup_view(request: HttpRequest) -> HttpResponse:
    """ユーザー登録（サインアップ）ビュー

    POSTリクエストの場合はフォームバリデーション後にユーザーを作成し、
    作成後に自動でログインさせてリダイレクトします。
    GETリクエストの場合は空のフォームを表示します。

    Args:
        request (HttpRequest): リクエストオブジェクト

    Returns:
        HttpResponse: サインアップページまたはリダイレクトレスポンス
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 作成後自動ログイン
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    """ユーザーログインビュー

    POSTリクエストの場合はフォームバリデーション後に認証を行い、
    認証成功かつユーザーが有効(is_active)であればログインしてリダイレクトします。
    認証失敗時はフォームにエラーを追加。
    GETリクエストの場合は空のフォームを表示します。

    Args:
        request (HttpRequest): リクエストオブジェクト

    Returns:
        HttpResponse: ログインページまたはリダイレクトレスポンス
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("home")
            form.add_error(None, "認証に失敗しました")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def home_view(request):
    """
    トップページ（FBV）

    - 未ログイン：ログインページへ
    - ログイン済み：タスク一覧へ
    """
    if request.user.is_authenticated:
        return redirect("tasks:task_list")
    return redirect("accounts:login")