# task_manager/tasks/views.py

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm


def task_list(request):
    """
    タスク一覧表示
    - フィルター: is_completed, is_archived
    - 検索: title, completed_comment
    - ソート: created_at降順
    """

    tasks = Task.objects.all().order_by('-created_at')

    # フィルター処理
    is_completed = request.GET.get('is_completed')
    is_archived = request.GET.get('is_archived')

    if is_completed in ['true', 'false']:
        tasks = tasks.filter(is_completed=(is_completed == 'true'))

    if is_archived in ['true', 'false']:
        tasks = tasks.filter(is_archived=(is_archived == 'true'))

    # 検索処理
    query = request.GET.get('q')
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
    タスク詳細表示
    """
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request: HttpRequest) -> HttpResponse:
    """
    新規タスク作成
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_update(request: HttpRequest, pk) -> HttpResponse:
    """
    既存タスクの編集
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


def task_delete(request: HttpRequest, pk) -> HttpResponse:
    """
    タスク削除
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})