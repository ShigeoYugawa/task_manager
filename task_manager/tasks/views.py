# task_manager/tasks/views.py

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Task
from .forms import TaskForm, TaskSearchForm
from .services import get_filtered_tasks


def task_list(request: HttpRequest) -> HttpResponse:
    """
    タスク一覧を表示する。
    TaskSearchFormで検索条件をバリデートし、get_filtered_tasksで
    条件に合うタスクを取得する。
    """

    # フォームにGETパラメータをバインド
    form = TaskSearchForm(request.GET)

    # フォームが有効なら cleaned_data から値を取得、無効ならデフォルト値
    if form.is_valid():
        is_completed = form.cleaned_data.get('is_completed')
        is_archived = form.cleaned_data.get('is_archived')
        query = form.cleaned_data.get('q', "")
    else:
        # 無効な場合も安全にデフォルト値を使用
        is_completed = None
        is_archived = None
        query = ""

    # サービス関数で条件に合致するタスクを取得
    tasks = get_filtered_tasks(
        is_completed=is_completed,
        is_archived=is_archived,
        q=query
    )

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'form': form,  # テンプレートでフォームを表示したい場合
    })


def task_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    タスク詳細を表示する。

    指定された主キーに対応するタスクを取得し、詳細ページをレンダリングします。

    Args:
        request (HttpRequest): リクエストオブジェクト
        pk (int): タスクの主キー

    Returns:
        HttpResponse: タスク詳細ページのレスポンス
    """
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request: HttpRequest) -> HttpResponse:
    """
    新規タスクを作成する。

    POSTリクエストの場合はフォームデータを保存し、タスク一覧へリダイレクト。
    GETリクエストの場合は空のフォームを表示します。

    Args:
        request (HttpRequest): リクエストオブジェクト

    Returns:
        HttpResponse: タスク作成ページまたはリダイレクト先のレスポンス
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_update(request: HttpRequest, pk: int) -> HttpResponse:
    """
    既存タスクを編集する。

    指定された主キーに対応するタスクを取得し、フォームで編集可能にする。
    POSTリクエストの場合は更新して詳細ページにリダイレクト。

    Args:
        request (HttpRequest): リクエストオブジェクト
        pk (int): 編集対象のタスクの主キー

    Returns:
        HttpResponse: タスク編集ページまたはリダイレクト先のレスポンス
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', pk=pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """
    タスクを削除する。

    指定された主キーに対応するタスクを取得し、POSTリクエストで削除してタスク一覧へリダイレクト。
    GETリクエストの場合は削除確認ページを表示します。

    Args:
        request (HttpRequest): リクエストオブジェクト
        pk (int): 削除対象のタスクの主キー

    Returns:
        HttpResponse: 削除確認ページまたはリダイレクト先のレスポンス
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
