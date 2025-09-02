
# Task Manager (PoC)

本リポジトリは、Django 5.2 を用いたタスク管理アプリケーションの **Proof of Concept (PoC)** 実装です。
小規模ながら、タスクの CRUD 操作、検索・フィルタ機能、管理画面対応、親子タスク構造までを網羅しています。

---

## 前提条件

* Python 3.12
* pip
* 仮想環境構築ツール `venv`
* Windows11 / WSL / Ubuntu 24.04
* VSCode

### Django インストール

```bash
pip install Django==5.2.5
````

### 型チェック・テスト関連

```bash
pip install mypy pytest pytest-django django-stubs django-stubs-ext
```

### gettext (i18n 用)

* macOS: `brew install gettext`
* Ubuntu / Debian: `sudo apt install gettext`
* Windows: [gettext for Windows](https://mlocati.github.io/articles/gettext-iconv-windows.html) をインストールし PATH に追加

---

## 主な機能（現状）

* タスク管理（CRUD）

  * タイトル、説明、作成日、更新日、完了状態、完了コメント、アーカイブ状態
  * 親子タスク構造を保持
* タスク一覧画面

  * **トップレベルタスクのみを表示**（子タスクは詳細ページで確認）
  * 検索・フィルタ

    * 完了状態・アーカイブ状態
    * タイトル・完了コメント部分一致検索
* タスク詳細ページ

  * 子タスク一覧を表示
* Django 管理画面

  * 完了状態を「完了 / 未完了」で表示
  * 検索・フィルタ対応
* ユーザー管理

  * Django 標準認証を利用
  * ユーザーごとのタスク表示・操作が可能
* ユニットテストでモデル・フォーム・ビュー・URL を網羅

---

## 技術スタック

* Python 3.12
* Django 5.2
* SQLite3（開発環境用）
* Bootstrap 5.3
* pytest + pytest-django
* mypy による型チェック
* gettext を使った i18n

---

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/<your-username>/task_manager.git
cd task_manager
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. Django マイグレーション

```bash
python manage.py migrate
```

### 5. 管理ユーザー作成

```bash
python manage.py createsuperuser
```

### 6. 開発サーバー起動

```bash
python manage.py runserver
```

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## mypy 型チェック

`mypy.ini` に設定済み:

```ini
[mypy]
python_version = 3.12
warn_unused_configs = True
ignore_missing_imports = True
strict = True

[mypy.plugins.django-stubs]
django_settings_module = "task_manager.settings"
```

実行:

```bash
mypy task_manager/tasks/
```

---

## pytest 設定

`pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = task_manager.settings
python_files = tests.py test_*.py *_tests.py
```

テスト実行:

```bash
pytest -v
```

---

## ディレクトリ構成（現状）

```bash
.
├── README.md
├── mypy.ini
├── pytest.ini
├── requirements.txt
└── task_manager/
    ├── accounts/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── templates/accounts/
    │   │   ├── login.html
    │   │   └── signup.html
    │   └── tests.py
    ├── db.sqlite3
    ├── locale/ja/LC_MESSAGES/
    │   ├── django.mo
    │   └── django.po
    ├── manage.py
    ├── task_manager/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── tasks/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── services.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── templates/tasks/
    │   │   ├── task_list.html
    │   │   ├── task_detail.html
    │   │   ├── task_form.html
    │   │   └── task_confirm_delete.html
    │   └── tests/
    │       ├── test_forms.py
    │       ├── test_models.py
    │       ├── test_services.py
    │       ├── test_urls.py
    │       ├── test_views.py
    │       └── test_views_crud.py
    └── templates/base.html
    └── uml/project_overview.puml
```

---

## 今後の展望

* Django REST Framework による API 化
* React などのフロントエンド分離構成
* Docker 化、および AWS デプロイ
* 権限管理・通知機能の追加
* 高度な検索・フィルタ、ダッシュボード表示
* 親子タスクのネスト構造の強化

---

## ライセンス

学習目的の PoC。無断再利用・配布不可。


