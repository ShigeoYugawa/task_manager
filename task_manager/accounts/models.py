# task_manager/accounts/models.py

from __future__ import annotations
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    カスタムユーザーマネージャー。ユーザー作成・スーパーユーザー作成を提供する。
    """

    def create_user(self, email: str, password: str = None, **extra_fields) -> CustomUser:
        """
        標準ユーザーを作成する。

        Args:
            email (str): ユーザーのメールアドレス
            password (str, optional): ユーザーパスワード
            **extra_fields: その他追加フィールド

        Raises:
            ValueError: email が未設定の場合

        Returns:
            CustomUser: 作成されたユーザーオブジェクト
        """
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # is_active はメール認証前は False に設定可能
        user.is_active = extra_fields.get("is_active", True)
        user.save(using=self._db)
        return user


    def create_superuser(self, email: str, password: str = None, **extra_fields) -> CustomUser:
        """スーパーユーザーを作成する。

        Args:
            email (str): ユーザーのメールアドレス
            password (str, optional): パスワード
            **extra_fields: その他追加フィールド

        Returns:
            CustomUser: 作成されたスーパーユーザー
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザー。

    Attributes:
        email (str): ログインに使用するメールアドレス
        nickname (str): 任意のニックネーム
        timezone (str): タイムゾーン（固定: Asia/Tokyo）
        is_admin (bool): システム管理権限
        can_edit (bool): 編集権限
        is_active (bool): Django標準のアクティブフラグ（メール認証前は False）
        is_staff (bool): Django管理画面アクセス用
        email_verified_at (datetime): メール認証完了日時
    """

    email = models.EmailField(verbose_name="メールアドレス", unique=True)
    nickname = models.CharField(verbose_name="ニックネーム", max_length=30, blank=True)
    first_name = models.CharField(verbose_name="名", max_length=30, blank=True)
    last_name = models.CharField(verbose_name="姓", max_length=30, blank=True)

    # 権限フラグ
    is_admin = models.BooleanField(verbose_name="システム管理権限", default=False)
    can_edit = models.BooleanField(verbose_name="編集権限", default=False)

    # Django 標準フラグ

    # メール認証導入前はログイン可能とする default=True
    # メール認証導入後は認証完了までログイン不可する default=False
    is_active = models.BooleanField(verbose_name="ログイン権限", default=True)

    is_staff = models.BooleanField(verbose_name="管理画面アクセス権限", default=False)

    # メール認証用タイムスタンプ
    email_verified_at = models.DateTimeField(verbose_name="メール認証完了日時", blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self) -> str:
        """
        画面表示

        - ニックネームを優先的に表示で使用する
        - ニックネームが未設定の場合は氏名を表示する
        - ニックネームと氏名が未設定の場合はe-mailを表示する
        """
        return (
            self.nickname
            or f"{self.last_name} {self.first_name}".strip()
            or self.email
        )


    def mark_email_verified(self) -> None:
        """メール認証完了時に呼び出す。

        このメソッドを呼ぶことで以下が実行される:
        - email_verified_at を現在時刻に設定
        - is_active を True に切り替え
        """
        self.email_verified_at = timezone.now()
        self.is_active = True
        self.save(update_fields=["email_verified_at", "is_active"])


    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー一覧"
