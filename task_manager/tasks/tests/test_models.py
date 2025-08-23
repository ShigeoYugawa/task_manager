# task_manager/tasks/tests/test_models.py

import pytest
from tasks.models import Task


@pytest.mark.django_db
class TestTaskModel:
    """
    Taskモデルに関する基本的なユニットテスト。
    - デフォルト値が正しく設定されるか
    - __str__ メソッドがタイトルを返すか
    """

    def test_create_task_with_defaults(self):
        """
        ✅ Task を title だけで作成した場合、
        他のフィールドが正しいデフォルト値で保存されることを確認する。
        """
        # Arrange: 必須フィールド title のみ指定
        task = Task.objects.create(title="Test Task")

        # Assert: デフォルト値の検証
        assert task.is_completed is False      # 完了状態は未完了
        assert task.is_archived is False       # アーカイブ状態は通常
        assert task.description == ""          # 説明は空文字
        assert task.completed_comment == ""    # 完了コメントは空文字

    def test_str_method_returns_title(self):
        """
        ✅ __str__ メソッドが title を返すことを確認する。
        """
        # Arrange
        task = Task.objects.create(title="Sample Task")

        # Act & Assert
        assert str(task) == "Sample Task"
