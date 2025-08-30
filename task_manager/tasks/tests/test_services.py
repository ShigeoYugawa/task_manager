# task_manager/tasks/tests/test_services.py

import pytest
from django.core.exceptions import ValidationError
from tasks.models import Task
from tasks.services import complete_task, reopen_task


@pytest.mark.django_db
class TestTaskServices:

    def test_complete_task_without_subtasks(self):
        """サブタスクなしのタスクを完了できることをテストする。

        条件:
            サブタスクが存在しないタスク
        行動:
            complete_task(task) を呼び出す
        期待結果:
            タスクの is_completed フィールドが True になる
        """
        task = Task.objects.create(title="親タスク")
        completed = complete_task(task)
        assert completed.is_completed is True



    def test_complete_task_with_incomplete_subtasks_raises_validation_error(self):
        """未完了のサブタスクがある場合、complete_task が ValidationError を発生させることをテストする。

        条件:
            親タスクに未完了の子タスクが存在する
        行動:
            complete_task(parent) を呼び出す
        期待結果:
            ValidationError が発生する
        """
        parent = Task.objects.create(title="親タスク")
        Task.objects.create(title="子タスク", parent=parent, is_completed=False)

        with pytest.raises(ValidationError):
            complete_task(parent)


    def test_complete_task_with_completed_subtasks(self):
        """すべてのサブタスクが完了済みの場合、親タスクを完了できることをテストする。

        条件:
            親タスクに完了済みの子タスクが複数存在する
        行動:
            complete_task(parent) を呼び出す
        期待結果:
            親タスクの is_completed フィールドが True になる
        """
        parent = Task.objects.create(title="親タスク")
        Task.objects.create(title="子タスク1", parent=parent, is_completed=True)
        Task.objects.create(title="子タスク2", parent=parent, is_completed=True)

        completed = complete_task(parent)
        assert completed.is_completed is True


    def test_reopen_task(self):
        """完了済みタスクを未完了に戻せることをテストする。

        条件:
            is_completed が True のタスク
        行動:
            reopen_task(task) を呼び出す
        期待結果:
            タスクの is_completed フィールドが False になる
        """
        task = Task.objects.create(title="完了済みタスク", is_completed=True)
        reopened = reopen_task(task)
        assert reopened.is_completed is False

