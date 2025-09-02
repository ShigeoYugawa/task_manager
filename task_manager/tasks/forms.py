# tasks/forms.py

from django import forms
from .models import Task
from django.core.exceptions import ValidationError
#from .services import complete_task

class TaskForm(forms.ModelForm):
    """
    タスク作成・編集用フォーム
    モデル Task を元に自動生成
    """

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'is_completed',
            'completed_comment',
            'is_archived',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'completed_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # 明示的に CheckboxInput にする
            'is_archived': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # 明示的に CheckboxInput にする
        }


def to_bool(value: str) -> bool:
    """
    TypedChoiceField 用の coerce 関数。
    "true" -> True
    "false" -> False
    空文字や None は空選択時に empty_value が適用されるのでここでは扱わない
    """
    value_lower = str(value).lower()
    if value_lower == "true":
        return True
    elif value_lower == "false":
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def clean(self):
    cleaned_data = super().clean()
    is_completed = cleaned_data.get("is_completed")
    task_instance = self.instance # Taskモデルを取得

    # 親タスクを完了しようとした場合、子タスクチェック
    if is_completed and task_instance.pk:
        if task_instance.subtasks.filter(is_completed=False).exists():
            raise ValidationError("子タスクが未完了のため、親タスクを完了できません。")

    return cleaned_data


class TaskSearchForm(forms.Form):
    """
    タスク検索フォーム。
    DB保存はせず、入力値のバリデーションと型変換だけを担当。
    """

    q = forms.CharField(
        required=False,
        label="検索キーワード",
        max_length=200,
        strip=True,
    )

    BOOLEAN_CHOICES = (
        ("", "---------"),
        ("true", "はい"),
        ("false", "いいえ"),
    )

    is_completed = forms.TypedChoiceField(
        choices=BOOLEAN_CHOICES,
        coerce=to_bool,
        required=False,
        label="完了状態",
        empty_value=None,  # 空選択時は None を返す
    )

    is_archived = forms.TypedChoiceField(
        choices=BOOLEAN_CHOICES,
        coerce=to_bool,
        required=False,
        label="アーカイブ済み",
        empty_value=None,  # 同様に None
    )