# tasks/forms.py

from django import forms
from .models import Task

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
            'is_archived'
        ]


class TaskSearchForm(forms.Form):
    """
    タスク検索フォーム。
    DB保存はせず、入力値のバリデーションと型変換だけを担当。
    """
    
    q = forms.CharField(
        required=False,
        label="検索キーワード",
        max_length=200,
        strip=True
    )
    is_completed = forms.NullBooleanField(
        required=False,
        label="完了状態"
    )
    is_archived = forms.NullBooleanField(
        required=False,
        label="アーカイブ済み"
    )