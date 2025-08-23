# task_manager/tasks/services.py

from django.db.models import Q
from django.db.models.query import QuerySet
from .models import Task


def get_filtered_tasks(
    q: str | None = None,
    is_completed: bool | None = None,
    is_archived: bool | None = None,
) -> QuerySet[Task]:
    """
    条件に合致した Task のクエリセットを返す。

    タスクは以下の条件で絞り込みや検索が可能です：
    - フィルター: is_completed, is_archived
    - 検索: title, completed_comment
    - ソート: created_at 降順

    Args:
        q (str | None): 検索キーワード。title または completed_comment を部分一致検索。
                        None または空文字の場合は検索条件に含めない。
        is_completed (bool | None): 完了状態でのフィルタ。
                        True または False の場合のみ条件に適用。
                        None の場合は無視する。
        is_archived (bool | None): アーカイブ状態でのフィルタ。
                        True または False の場合のみ条件に適用。
                        None の場合は無視する。

    Returns:
        QuerySet[Task]: 検索条件に合致した Task のクエリセット。
    """
    # すべてのタスクを対象に開始（作成日時降順）
    tasks = Task.objects.all().order_by("-created_at")

    # キーワード検索（タイトル・完了コメントの部分一致）
    if q:
        tasks = tasks.filter(
            Q(title__icontains=q) |
            Q(completed_comment__icontains=q)
        )

    # 完了状態でフィルタ
    if is_completed is not None:
        tasks = tasks.filter(is_completed=is_completed)

    # アーカイブ状態でフィルタ
    if is_archived is not None:
        tasks = tasks.filter(is_archived=is_archived)

    return tasks
