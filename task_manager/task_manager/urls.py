# task_manager/task_manager/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # アカウント機能（UI）
    path("accounts/", include("accounts.urls")),
    # タスク機能（UI）
    path("tasks/", include("tasks.urls")),
    path('', accounts_views.home_view, name='home'),


    # task_manager/views.pyを作成してhome/を設置する
    #
    path("home/", views.user_home, name="user_home"),

    # APIエンドポイント
    path("api/accounts/", include("accounts.api.urls")),
    path("api/tasks/", include("tasks.api.urls")),
    path('api-auth/', include('rest_framework.urls')),
]
