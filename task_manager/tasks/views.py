# task_manager/tasks/views.py

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Task
from .forms import TaskForm


def task_list(request: HttpRequest) -> HttpResponse:
    """
    タスク一覧を表示する。

    タスクは以下の条件で絞り込みや検索が可能です：
        - フィルター: is_completed, is_archived
        - 検索: title, completed_comment
        - ソート: created_at降順

    想定URL例:
        ?is_completed=true&is_archived=false&q=python

    注意:
        - 軽量のレコードに限りこのコードは有効です。
        - 大量レコードの場合は専用検索エンジン
          (Elasticsearch, PostgreSQLのGIN index など) を使用する必要があります。

    Args:
        request (HttpRequest): リクエストオブジェクト

    Returns:
        HttpResponse: タスク一覧ページのレスポンス
    """

    tasks = Task.objects.all().order_by('-created_at')

    # フィルター処理(URLパラメーターから取得)
    is_completed = request.GET.get('is_completed')
    is_archived = request.GET.get('is_archived')

    # 文字列からBooleanを生成する
    if is_completed in ['true', 'false']:
        tasks = tasks.filter(is_completed=(is_completed == 'true'))

    if is_archived in ['true', 'false']:
        tasks = tasks.filter(is_archived=(is_archived == 'true'))

    # 検索処理（ここでは単純な文字検索を行っているため、大量データでは別のアプローチが必要）
    query = request.GET.get('q', '').strip()
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(completed_comment__icontains=query)
        )

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'is_completed': is_completed,
        'is_archived': is_archived,
        'query': query,
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
