# tasks/admin.py

from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    管理画面で Task モデルを操作するための設定。

    - list_display: 一覧画面に表示する列を指定
        'title'        : タスク名
        'status'       : 完了状態（カスタムメソッド）
        'is_archived'  : アーカイブ状態
        'created_at'   : 作成日時
        'updated_at'   : 最終更新日

    - list_filter: 絞り込み用のフィルター
        'is_completed' : 完了済み / 未完了
        'is_archived'  : アーカイブ済み / 通常タスク

    - search_fields: 検索対象フィールド
        'title'            : タスク名
        'completed_comment' : 完了時コメント

    - ordering: 一覧のデフォルトソート順
        '-created_at' : 最新作成順
    """

    list_display = ('title', 'status', 'is_archived', 'created_at', 'updated_at')
    list_filter = ('is_completed', 'is_archived')
    search_fields = ('title', 'completed_comment')
    ordering = ('-created_at',)

    def status(self, obj):
        """
        完了状態を文字で表示するカスタム列。
        - 完了済みの場合は "完了"
        - 未完了の場合は "未完了"
        """
        return "完了" if obj.is_completed else "未完了"

    # 管理画面上の列名として表示
    status.short_description = "状態"
