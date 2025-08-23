# task_manager/tasks/tests/test_views.py

import pytest
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
class TestTaskListView:
    """Task一覧ビューの動作確認"""

    def test_list_all_tasks(self, client):
        # Arrange: 2件のタスクを作成
        Task.objects.create(title="Task A")
        Task.objects.create(title="Task B")

        # Act: タスク一覧ページを取得
        url = reverse("tasks:task_list")
        response = client.get(url)

        # Assert: 両方のタスクが表示されることを確認
        assert response.status_code == 200
        assert "Task A" in response.content.decode()
        assert "Task B" in response.content.decode()

    def test_filter_by_completed(self, client):
        # Arrange: 完了済み・未完了タスクを作成
        Task.objects.create(title="Done", is_completed=True)
        Task.objects.create(title="Todo", is_completed=False)

        # Act: 完了済みフィルタを付けてページ取得
        url = reverse("tasks:task_list")
        response = client.get(url, {"is_completed": "true"})

        # Assert: 完了済みタスクのみ表示されること
        assert "Done" in response.content.decode()
        assert "Todo" not in response.content.decode()

    def test_search_query(self, client):
        # Arrange: 複数タスクを作成
        Task.objects.create(title="Learn Django")
        Task.objects.create(title="Write Flask app")

        # Act: "Django" 検索クエリでページ取得
        url = reverse("tasks:task_list")
        response = client.get(url, {"q": "Django"})

        # Assert: 検索結果に Django タスクのみ表示されること
        assert "Learn Django" in response.content.decode()
        assert "Flask" not in response.content.decode()
