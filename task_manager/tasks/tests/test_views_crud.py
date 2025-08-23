# task_manager/tasks/tests/test_views_crud.py

import pytest
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
class TestTaskCRUDViews:
    """タスク作成・更新・削除・詳細ビューのテスト"""

    def test_task_detail_view(self, client):
        # Arrange: タスク作成
        task = Task.objects.create(title="詳細確認タスク")

        # Act: タスク詳細ページにアクセス
        url = reverse("tasks:task_detail", args=[task.pk])
        response = client.get(url)

        # Assert: ページが正しく表示され、コンテキストにタスクが渡される
        assert response.status_code == 200
        assert "詳細確認タスク" in response.content.decode()
        assert response.context["task"].pk == task.pk

    def test_task_create_view_get(self, client):
        # Act: GETリクエストでタスク作成ページを表示
        url = reverse("tasks:task_create")
        response = client.get(url)

        # Assert: ページが正しく表示され、フォームがコンテキストに渡される
        assert response.status_code == 200
        assert "form" in response.context

    def test_task_create_view_post(self, client):
        # Arrange: POSTデータ準備
        data = {
            "title": "新規作成タスク",
            "description": "説明",
            "is_completed": False,
            "completed_comment": "",
            "is_archived": False
        }

        # Act: POSTリクエストでタスク作成
        url = reverse("tasks:task_create")
        response = client.post(url, data)

        # Assert: 作成後にタスク一覧へリダイレクトされ、DBに保存されている
        assert response.status_code == 302
        task = Task.objects.get(title="新規作成タスク")
        assert task.description == "説明"

    def test_task_update_view_get(self, client):
        # Arrange: タスク作成
        task = Task.objects.create(title="更新前タスク")

        # Act: GETリクエストで編集ページを表示
        url = reverse("tasks:task_update", args=[task.pk])
        response = client.get(url)

        # Assert: ページが表示され、フォームにタスクデータが設定される
        assert response.status_code == 200
        assert "form" in response.context

    def test_task_update_view_post(self, client):
        # Arrange: タスク作成
        task = Task.objects.create(title="更新前タスク")

        # Act: POSTリクエストでタスク更新
        data = {
            "title": "更新後タスク",
            "description": "更新説明",
            "is_completed": True,
            "completed_comment": "完了",
            "is_archived": False
        }
        url = reverse("tasks:task_update", args=[task.pk])
        response = client.post(url, data)

        # Assert: 更新後に詳細ページへリダイレクトされ、DBの値が更新されている
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == "更新後タスク"
        assert task.is_completed is True
        assert task.completed_comment == "完了"

    def test_task_delete_view_get(self, client):
        # Arrange: タスク作成
        task = Task.objects.create(title="削除確認タスク")

        # Act: GETリクエストで削除確認ページを表示
        url = reverse("tasks:task_delete", args=[task.pk])
        response = client.get(url)

        # Assert: ページが表示され、削除対象タスクがコンテキストに渡される
        assert response.status_code == 200
        assert "削除確認タスク" in response.content.decode()
        assert response.context["task"].pk == task.pk

    def test_task_delete_view_post(self, client):
        # Arrange: タスク作成
        task = Task.objects.create(title="削除対象タスク")

        # Act: POSTリクエストでタスク削除
        url = reverse("tasks:task_delete", args=[task.pk])
        response = client.post(url)

        # Assert: 削除後にタスク一覧へリダイレクトされ、DBから削除されている
        assert response.status_code == 302
        assert not Task.objects.filter(pk=task.pk).exists()
