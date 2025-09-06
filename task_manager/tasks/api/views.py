# task_manager/tasks/api/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ..models import Task


# ------------------------------------
# 簡素版
# ------------------------------------
@require_GET
def task_list_api_simple(request):
    """
    学習用の簡素版タスク一覧API
    - is_completed=true/false のみサポート
    - title / created_at / is_completed を返す
    """
    tasks = Task.objects.all()

    is_completed = request.GET.get("is_completed")
    if is_completed in ["true", "false"]:
        tasks = tasks.filter(is_completed=(is_completed == "true"))

    # forを使った基本的なリスト作成
    data = []
    for task in tasks:
        data.append({
            "title": task.title,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "is_completed": task.is_completed,
        })

    # リスト内包表記版
    #data = [
    #    {
    #        "title": task.title,
    #        "created_at": task.created_at.isoformat() if task.created_at else None,
    #        "is_completed": task.is_completed,
    #    }
    #    for task in tasks
    #]

    return JsonResponse(data, safe=False)


def task_preview(request):
    """
    簡素版 Ajax 検索画面のレンダリング用
    """
    return render(request, "tasks_api/task_search_ajax_simple.html")


# ------------------------------------
# 運用版
# ------------------------------------
@require_GET
def task_list_api(request):
    """
    タスク一覧を条件付きでJSON形式で返すAPI
    クエリパラメータ例:
    - is_completed=true/false
    - is_archived=true/false
    - user_id=1
    """
    tasks = Task.objects.all()

    # --- フィルタリング処理 ---
    is_completed = request.GET.get("is_completed")
    if is_completed is not None:
        tasks = tasks.filter(is_completed=is_completed.lower() == "true")

    is_archived = request.GET.get("is_archived")
    if is_archived is not None:
        tasks = tasks.filter(is_archived=is_archived.lower() == "true")

    user_id = request.GET.get("user_id")
    if user_id is not None and user_id.isdigit():
        tasks = tasks.filter(user_id=int(user_id))

    # --- JSON 変換 ---
    data = []
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            "is_archived": task.is_archived,
            "completed_comment": task.completed_comment,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
            "parent_id": task.parent_id,
            "user_id": task.user_id,
        })

    return JsonResponse({"tasks": data})


@require_GET
def task_list_by_completion(request, is_completed: str):
    """URLパラメータで完了状態を指定してタスク一覧を返す"""
    tasks = Task.objects.filter(is_completed=(is_completed.lower() == "true"))

    data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            "is_archived": task.is_archived,
            "completed_comment": task.completed_comment,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
            "parent_id": task.parent_id,
            "user_id": task.user_id,
        }
        for task in tasks
    ]
    return JsonResponse({"tasks": data})


@require_GET
def task_list_by_user(request, user_id: int):
    """URLパラメータでユーザーを指定してタスク一覧を返す"""
    tasks = Task.objects.filter(user_id=user_id)

    data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            "is_archived": task.is_archived,
            "completed_comment": task.completed_comment,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
            "parent_id": task.parent_id,
            "user_id": task.user_id,
        }
        for task in tasks
    ]
    return JsonResponse({"tasks": data})