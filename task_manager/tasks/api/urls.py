# task_manager/tasks/urls.py

from django.urls import path
from . import views

app_name = "tasks_api"

urlpatterns = [
    # --- API ---

    # クエリパラメータ版 (例: /api/tasks/?is_completed=true)
    path("", views.task_list_api, name="task_list"),
    # 簡素版学習用API (例: /api/tasks/simple/?is_completed=true)
    path("simple/", views.task_list_api_simple, name="task_list_simple"),    
    # URLパラメータ版 (例: /api/tasks/completed/true/)
    path("completed/<str:is_completed>/", views.task_list_by_completion, name="task_list_by_completion"),
    # URLパラメータでユーザー別取得 (例: /api/tasks/user/1/)
    path("user/<int:user_id>/", views.task_list_by_user, name="task_list_by_user"),


    # --- HTML画面 ---
    
    path("preview/", views.task_preview, name="task_preview"),
]
