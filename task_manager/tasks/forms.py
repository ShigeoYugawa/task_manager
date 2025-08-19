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