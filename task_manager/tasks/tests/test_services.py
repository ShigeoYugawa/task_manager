# task_manager/tasks/tests/test_services.py

import pytest
from django.core.exceptions import ValidationError
from tasks.models import Task
from tasks.services import complete_task, reopen_task


@pytest.mark.django_db
class TestTaskServices:

    def test_complete_task_without_subtasks(self):
        """サブタスクなしでタスクを完了できる"""
        task = Task.objects.create(title="親タスク")
        completed = complete_task(task)
        assert completed.is_completed is True

    def test_complete_task_with_incomplete_subtasks_raises_validation_error(self):
        """サブタスクが未完了の場合、ValidationError が発生する"""
        parent = Task.objects.create(title="親タスク")
        Task.objects.create(title="子タスク", parent=parent, is_completed=False)

        with pytest.raises(ValidationError):
            complete_task(parent)

    def test_complete_task_with_completed_subtasks(self):
        """サブタスクがすべて完了済みの場合、タスクを完了できる"""
        parent = Task.objects.create(title="親タスク")
        Task.objects.create(title="子タスク1", parent=parent, is_completed=True)
        Task.objects.create(title="子タスク2", parent=parent, is_completed=True)

        completed = complete_task(parent)
        assert completed.is_completed is True

    def test_reopen_task(self):
        """完了済みタスクを未完了に戻す"""
        task = Task.objects.create(title="完了済みタスク", is_completed=True)
        reopened = reopen_task(task)
        assert reopened.is_completed is False
