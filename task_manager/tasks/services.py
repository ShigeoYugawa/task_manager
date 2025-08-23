# task_manager/tasks/services.py

from django.db.models import Q
from django.db.models.query import QuerySet
from .models import Task

def get_filtered_tasks(
    is_completed: bool | None = None,
    is_archived: bool | None = None,
    query: str = ""
) -> QuerySet[Task]:
    
    """
    条件に合致したTaskリストを返す。

    タスクは以下の条件で絞り込みや検索が可能です：
    - フィルター: is_completed, is_archived
    - 検索: title, completed_comment
    - ソート: created_at降順

    Args:
        is_completed: 完了済フラグ 
        is_archived:  アーカイブ済フラグ  
        query:        クエリ文字列

    Returns:
        QuerySet[Task]: クエリセット
    """

    tasks = Task.objects.all().order_by('-created_at')

    if is_completed is not None:
        tasks = tasks.filter(is_completed=is_completed)
    if is_archived is not None:
        tasks = tasks.filter(is_archived=is_archived)
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | 
            Q(completed_comment__icontains=query))
    
    return tasks
