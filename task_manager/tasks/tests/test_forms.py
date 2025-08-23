# task_manager/tasks/tests/test_forms.py

from django.test import TestCase
from tasks.forms import TaskSearchForm


class TaskSearchFormTestCase(TestCase):
    """TaskSearchForm のバリデーションテスト"""

    def test_valid_data(self):
        # Arrange: 正常なフォームデータを用意
        form = TaskSearchForm({
            "q": "python",
            "is_completed": "true",
            "is_archived": "false",
        })

        # Act & Assert: フォームが有効か確認
        self.assertTrue(form.is_valid())
        # Assert: cleaned_data が期待通りに変換されていることを確認
        self.assertEqual(form.cleaned_data["q"], "python")
        self.assertTrue(form.cleaned_data["is_completed"])   # "true" → True
        self.assertFalse(form.cleaned_data["is_archived"])   # "false" → False

    def test_empty_data(self):
        # Arrange: 空データを用意
        form = TaskSearchForm({})

        # Act & Assert: フォームが有効であること
        self.assertTrue(form.is_valid())
        # Assert: デフォルト値が適切に設定されることを確認
        self.assertEqual(form.cleaned_data["q"], "")
        self.assertIsNone(form.cleaned_data["is_completed"])
        self.assertIsNone(form.cleaned_data["is_archived"])

    def test_invalid_boolean(self):
        # Arrange: 不正なブール値を与える
        form = TaskSearchForm({"is_completed": "maybe"})

        # Act & Assert: フォームは無効になること
        self.assertFalse(form.is_valid())
