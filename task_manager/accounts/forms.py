# task_manager/accounts/forms.py

from __future__ import annotations
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """
    ユーザー作成用フォーム。（管理画面表示で必須）

    Django 管理画面やカスタムビューから新しいユーザーを作成する際に利用される。
    2つのパスワード入力欄を持ち、両者が一致することを検証する。
    """

    password1 = forms.CharField(
        label="パスワード", widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="パスワード（確認）", widget=forms.PasswordInput
    )


    class Meta:
        """フォームに含めるフィールドを定義。"""
        model = CustomUser
        fields = (
            "email",
            "nickname",
            "first_name",
            "last_name",
            "is_admin",
            "can_edit")


    def clean_password2(self) -> str:
        """2つのパスワード入力欄が一致するか検証する。

        Raises:
            forms.ValidationError: パスワードが一致しない場合

        Returns:
            str: 検証済みのパスワード（password2）
        """
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return p2


    def save(self, commit: bool = True) -> CustomUser:
        """新しいユーザーを保存する。

        Args:
            commit (bool, optional): データベースへ即保存するかどうか。Defaults to True.

        Returns:
            CustomUser: 作成されたユーザーオブジェクト
        """
        user = super().save(commit=False)
        # パスワードハッシュ化は必ず set_password
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """
    ユーザー更新用フォーム。（管理画面表示で必須）

    管理画面からユーザー情報を編集する際に利用される。
    パスワードは変更不可で、ハッシュ化済み値を読み取り専用として表示する。
    """

    password = ReadOnlyPasswordHashField(label="パスワード")


    class Meta:
        """フォームに含めるフィールドを定義。"""
        model = CustomUser
        fields = (
            "email",
            "nickname",
            "first_name",
            "last_name",
            "password",
            "is_admin",
            "can_edit",
            "is_active",
            "is_staff",
        )


class SignUpForm(forms.ModelForm):
    """ユーザー登録用フォーム（フロント向け）"""

    password1 = forms.CharField(
        label="パスワード", widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="パスワード（確認）", widget=forms.PasswordInput
    )


    class Meta:
        model = CustomUser
        fields = ("email", "nickname")


    def clean_password2(self) -> str:
        """パスワード確認の検証"""
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("パスワードが一致しません。")
        return p2


    def save(self, commit: bool = True) -> CustomUser:
        """ユーザー作成"""
        user = super().save(commit=False)
        # パスワードハッシュ化は必ず set_password
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    """ユーザーログインフォーム"""

    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(
        label="パスワード", widget=forms.PasswordInput
    )