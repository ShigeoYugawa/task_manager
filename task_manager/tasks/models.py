# tasks/models.py

from django.conf import settings
from django.db import models

class Task(models.Model):
    """
    ユーザーが管理するタスクを表すモデル。

    フィールド:
    - title: タスク名
    - is_completed: タスクの完了状態（True: 完了、False: 未完了）
    - created_at: タスク作成日時（自動で設定）
    - completed_comment: 完了時のコメント（任意）
    - is_archived: タスクのアーカイブ状態（True: アーカイブ済み、False: 通常タスク）
    """

    # タスクのタイトル（必須）
    title = models.CharField(verbose_name="タスク名", max_length=200)
    
    # タスクの詳細説明
    description = models.TextField(verbose_name="タスク詳細", blank=True)

    # タスクの完了状態。デフォルトは未完了
    is_completed = models.BooleanField(verbose_name="タスクの完了状態", default=False)
    
    # タスク作成日時。オブジェクト作成時に自動設定
    created_at = models.DateTimeField(verbose_name="タスク作成日時", auto_now_add=True)

    # 最終更新日時。更新時に自動で書き換わる
    updated_at = models.DateTimeField(verbose_name="最終更新日時", auto_now=True)
    
    # 完了時に記録するコメント（任意）。空でもOK
    completed_comment = models.CharField(verbose_name="完了時に記録するコメント（任意）", max_length=200, blank=True)
    
    # タスクをアーカイブするかどうか。デフォルトは通常タスク
    is_archived = models.BooleanField(verbose_name="タスクをアーカイブする", default=False)

    # 親タスク
    parent = models.ForeignKey("self", verbose_name="親タスク", on_delete=models.CASCADE, related_name="subtasks", null=True, blank=True)

    # ユーザーとの紐づけ
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # カスタムユーザーを参照
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,  # 一時的に必須でない
        blank=True
    )


    def __str__(self) -> str:
        """
        管理画面やシェルでタスクオブジェクトを表示した際の文字列
        タスクタイトルを返す
        """
        return self.title


    class Meta:
        verbose_name = "タスク"
        verbose_name_plural = "タスク一覧"