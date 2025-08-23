# task_manager/tasks/tests/test_urls.py

from django.urls import reverse, resolve
from tasks import views


class TestTaskUrls:
    """
    tasks/urls.py の URL パターンが
    それぞれ正しいビュー関数に解決されることを確認する。
    """

    def test_task_list_url(self):
        # Arrange & Act
        path = reverse("tasks:task_list")

        # Assert
        assert resolve(path).func == views.task_list

    def test_task_detail_url(self):
        # Arrange & Act
        path = reverse("tasks:task_detail", kwargs={"pk": 1})

        # Assert
        assert resolve(path).func == views.task_detail

    def test_task_create_url(self):
        # Arrange & Act
        path = reverse("tasks:task_create")

        # Assert
        assert resolve(path).func == views.task_create

    def test_task_update_url(self):
        # Arrange & Act
        path = reverse("tasks:task_update", kwargs={"pk": 1})

        # Assert
        assert resolve(path).func == views.task_update

    def test_task_delete_url(self):
        # Arrange & Act
        path = reverse("tasks:task_delete", kwargs={"pk": 1})

        # Assert
        assert resolve(path).func == views.task_delete
