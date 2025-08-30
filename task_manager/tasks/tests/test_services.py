# task_manager/tasks/tests/test_services.py

import pytest
from django.core.exceptions import ValidationError
from tasks.models import Task
from tasks.services import get_filtered_tasks, complete_task, reopen_task


@pytest.mark.django_db
class TestTaskServices:

    # -------------------
    # complete_task 系
    # -------------------
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

    # -------------------
    # reopen_task 系
    # -------------------
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

    # -------------------
    # get_filtered_tasks 系
    # -------------------
    def test_get_filtered_tasks_returns_all_tasks_when_no_filters_applied(self):
        """フィルタ未指定時に全タスクが作成日時降順で返ることをテストする。

        条件:
            複数のタスクが存在する
        行動:
            get_filtered_tasks() を呼び出す
        期待結果:
            すべてのタスクが created_at 降順で返る
        """
        t1 = Task.objects.create(title="古いタスク")
        t2 = Task.objects.create(title="新しいタスク")

        tasks = list(get_filtered_tasks())
        assert tasks == [t2, t1]

    def test_get_filtered_tasks_filters_by_title_keyword(self):
        """タイトルに部分一致でマッチするタスクのみ返ることをテストする。

        条件:
            title に「報告」を含むタスクと含まないタスクが存在する
        行動:
            get_filtered_tasks(q="報告") を呼び出す
        期待結果:
            title に「報告」を含むタスクのみ返る
        """
        match = Task.objects.create(title="報告書作成")
        Task.objects.create(title="打ち合わせ")

        tasks = list(get_filtered_tasks(q="報告"))
        assert tasks == [match]

    def test_get_filtered_tasks_filters_by_completed_status(self):
        """完了状態でフィルタできることをテストする。

        条件:
            完了タスクと未完了タスクが存在する
        行動:
            get_filtered_tasks(is_completed=True) を呼び出す
        期待結果:
            完了タスクのみ返る
        """
        done = Task.objects.create(title="完了タスク", is_completed=True)
        Task.objects.create(title="未完了タスク", is_completed=False)

        tasks = list(get_filtered_tasks(is_completed=True))
        assert tasks == [done]

    def test_get_filtered_tasks_filters_by_archived_status(self):
        """アーカイブ状態でフィルタできることをテストする。

        条件:
            アーカイブ済みタスクと未アーカイブタスクが存在する
        行動:
            get_filtered_tasks(is_archived=True) を呼び出す
        期待結果:
            アーカイブ済みタスクのみ返る
        """
        archived = Task.objects.create(title="アーカイブ済み", is_archived=True)
        Task.objects.create(title="通常タスク", is_archived=False)

        tasks = list(get_filtered_tasks(is_archived=True))
        assert tasks == [archived]

    def test_get_filtered_tasks_combined_filters(self):
        """キーワード + 完了状態 + アーカイブ状態で複合フィルタが正しく動作することをテストする。

        条件:
            複数のタスクが存在する
            - タイトルに "報告" を含むタスク
            - 完了済みかつ未アーカイブのタスク
        行動:
            get_filtered_tasks(q="報告", is_completed=True, is_archived=False) を呼び出す
        期待結果:
            キーワード部分一致かつ完了済みかつ未アーカイブのタスクのみ返る
        """
        # データ作成
        match1 = Task.objects.create(title="報告書作成", is_completed=True, is_archived=False)
        match2 = Task.objects.create(title="報告済みタスク", is_completed=True, is_archived=False)
        Task.objects.create(title="報告書作成", is_completed=False, is_archived=False)  # 未完了
        Task.objects.create(title="報告書作成", is_completed=True, is_archived=True)   # アーカイブ済み

        tasks = list(get_filtered_tasks(q="報告", is_completed=True, is_archived=False))

        # OR 条件検索 + 完了済み + 未アーカイブ にマッチするタスクのみ
        expected_tasks = {match1, match2}
        assert set(tasks) == expected_tasks

