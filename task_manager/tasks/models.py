# tasks/models.py

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
    title = models.CharField(max_length=200)
    
    # タスクの詳細説明
    description = models.TextField(blank=True)

    # タスクの完了状態。デフォルトは未完了
    is_completed = models.BooleanField(default=False)
    
    # タスク作成日時。オブジェクト作成時に自動設定
    created_at = models.DateTimeField(auto_now_add=True)

    # 最終更新日時。更新時に自動で書き換わる
    updated_at = models.DateTimeField(auto_now=True)
    
    # 完了時に記録するコメント（任意）。空でもOK
    completed_comment = models.CharField(max_length=200, blank=True)
    
    # タスクをアーカイブするかどうか。デフォルトは通常タスク
    is_archived = models.BooleanField(default=False)


    def __str__(self) -> str:
        """
        管理画面やシェルでタスクオブジェクトを表示した際の文字列
        タスクタイトルを返す
        """
        return self.title


    class Meta:
        verbose_name = "タスク"
        verbose_name_plural = "タスク一覧"