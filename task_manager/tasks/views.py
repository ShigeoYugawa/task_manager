# task_manager/tasks/views.py

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages 
from django.db.models import Q
from .models import Task
from .forms import TaskForm, TaskSearchForm
from .services import get_filtered_tasks, complete_task 


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

    # 条件に合致するタスクを取得し、親がないタスクのみに絞る
    tasks = get_filtered_tasks(
        is_completed=is_completed,
        is_archived=is_archived,
        q=query
    ).filter(parent__isnull=True, user=request.user) # ユーザーで絞る

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "form": form,
        "query": query,
        "is_completed": form.data.get("is_completed"),
        "is_archived": form.data.get("is_archived"),
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
    subtasks = task.subtasks.all().order_by('-created_at')  # 子タスク一覧（作成日降順）
    has_incomplete_subtasks = task.subtasks.filter(is_completed=False).exists()

    return render(
        request,
        'tasks/task_detail.html',
        {
            'task': task,
            'subtasks': subtasks,
            'has_incomplete_subtasks': has_incomplete_subtasks,  # ← 渡す
        }
    )


@login_required
def task_create(request: HttpRequest, parent_pk: int | None = None) -> HttpResponse:
    """
    新規タスクを作成する。

    POSTリクエストの場合はフォームデータを保存し、タスク一覧へリダイレクト。
    GETリクエストの場合は空のフォームを表示します。

    Args:
        request (HttpRequest): リクエストオブジェクト

    Returns:
        HttpResponse: タスク作成ページまたはリダイレクト先のレスポンス
    """
    parent_task = None
    if parent_pk:
        parent_task = get_object_or_404(Task, pk=parent_pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # ← ログインユーザーを紐づけ
            if parent_task:
                task.parent = parent_task            
            form.save()
            if parent_task:
                return redirect('tasks:task_detail', pk=parent_task.pk)            
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
        
    return render(request, 'tasks/task_form.html', {'form': form, 'parent_task': parent_task})


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
    task = get_object_or_404(Task, pk=pk, user=request.user)
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


def task_complete(request: HttpRequest, pk: int) -> HttpResponse:
    """
    タスクを完了状態に変更する。
    子タスクが未完了の場合はエラーを表示して詳細画面へ戻す。
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        try:
            complete_task(task)
            messages.success(request, "タスクを完了にしました。")
        except ValidationError as e:
            messages.error(request, f"完了できません: {e.message}")
        return redirect("tasks:task_detail", pk=pk)

    # POST 以外は詳細画面へ
    return redirect("tasks:task_detail", pk=pk)