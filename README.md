
---

# Task Manager (PoC)

本リポジトリは、Django 5.2 を用いたタスク管理アプリケーションの **Proof of Concept (PoC)** 実装です。
小規模ながら、タスクの CRUD 操作、検索・フィルタ機能、管理画面対応まで網羅しています。

---

## 前提条件

このプロジェクトをセットアップ・実行するには、以下の環境が必要です。

### 1. システム・Python関連

- Python 3.12 がインストール済み
  [公式サイト](https://www.python.org/downloads/) から入手可能
- pip が利用可能
- 仮想環境構築ツール `venv` が利用可能
- Windows11/WSL/Ubuntu-24.04
- VSCode

### 2. Django関連

* Django 5.2 がインストール済み

  ```bash
  pip install Django==5.2.5
  ```

### 3. gettext (i18n 用)

Django の国際化機能を利用するには gettext が必要です。

* macOS:

  ```bash
  brew install gettext
  ```
* Ubuntu / Debian:

  ```bash
  sudo apt install gettext
  ```
* Windows:

  * [gettext for Windows](https://mlocati.github.io/articles/gettext-iconv-windows.html) からインストール
  * 環境変数 PATH に追加

### 4. 型チェック・テスト関連

* mypy（型チェック）
* pytest + pytest-django（ユニットテスト）

  ```bash
  pip install mypy pytest pytest-django django-stubs django-stubs-ext
  ```

---

## 主な機能（現状）

* タスク管理（CRUD）

  * タイトル、説明、作成日、更新日、完了状態、完了コメント、アーカイブ状態
* タスク一覧画面での検索・フィルタ

  * 完了状態・アーカイブ状態の絞り込み
  * タイトル・完了コメントの部分一致検索
* 管理画面 (Django Admin) でのタスク管理

  * 完了状態を「完了 / 未完了」で表示
  * 検索・フィルタ対応
* ユニットテストでモデル・フォーム・ビュー・URL を網羅

※ ユーザー管理は Django 標準認証を使用しており、現時点ではユーザーごとのタスク制御は未実装。

---

## 技術スタック

* Python 3.12
* Django 5.2
* SQLite3 (開発環境用)
* Bootstrap 5.3
* pytest + pytest-django によるユニットテスト
* mypy による型チェック
* gettext を使った国際化 (i18n) 用 `.po` / `.mo` ファイル

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

#### 依存パッケージ例（requirements.txt）

```
asgiref==3.9.1
Django==5.2.5
django-stubs==5.2.2
django-stubs-ext==5.2.2
iniconfig==2.1.0
mypy==1.17.1
mypy_extensions==1.1.0
packaging==25.0
pathspec==0.12.1
pluggy==1.6.0
Pygments==2.19.2
pytest==8.4.1
pytest-django==4.11.1
sqlparse==0.5.3
types-PyYAML==6.0.12.20250809
typing_extensions==4.14.1
```

### 4. Django マイグレーションの実行

```bash
python manage.py migrate
```

### 5. 管理ユーザーの作成

```bash
python manage.py createsuperuser
```

### 6. 開発サーバーの起動

```bash
python manage.py runserver
```

[http://127.0.0.1:8000/](http://127.0.0.1:8000/) でアプリケーションにアクセス可能です。

---

## mypy 型チェック

`mypy.ini` または `setup.cfg` に以下を追加：

```ini
[mypy]
python_version = 3.12
warn_unused_configs = True
ignore_missing_imports = True
strict = True

[mypy.plugins.django-stubs]
django_settings_module = "task_manager.settings"
```

型チェック実行：

```bash
mypy tasks/
```

---

## pytest 設定

`pytest.ini` に Django 設定を指定：

```ini
[pytest]
DJANGO_SETTINGS_MODULE = task_manager.settings
python_files = tests.py test_*.py *_tests.py
```

テスト実行：

```bash
pytest -v
```

---

## 国際化 (i18n) の導入

1. メッセージファイル作成（例: 日本語）

```bash
django-admin makemessages -l ja
```

`locale/ja/LC_MESSAGES/django.po` が生成されます。翻訳文を記入後、コンパイル：

```bash
django-admin compilemessages
```

`django.mo` が生成され、Django が翻訳を反映します。

2. 翻訳をテンプレートやコードで使用

```python
from django.utils.translation import gettext as _

verbose_name = _("タスク")
```

テンプレートでは：

```html
{% load i18n %}
<h1>{% trans "タスク一覧" %}</h1>
```

---

## ディレクトリ構成（概要）

```bash
task_manager/
├── README.md
├── requirements.txt
├── mypy.ini
├── pytest.ini
├── manage.py
├── db.sqlite3
├── locale/
│   └── ja/LC_MESSAGES/
│       ├── django.po
│       └── django.mo
├── task_manager/       # プロジェクト設定
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/           # ユーザー管理アプリ
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── tasks/              # タスク管理アプリ
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── services.py
    ├── urls.py
    ├── views.py
    ├── templates/
    │   └── tasks/
    │       ├── task_list.html
    │       ├── task_detail.html
    │       ├── task_form.html
    │       └── task_confirm_delete.html
    └── tests/
        ├── test_forms.py
        ├── test_models.py
        ├── test_urls.py
        ├── test_views.py
        └── test_views_crud.py
```

---

## 今後の展望

* ユーザーごとのタスク管理
* Django REST Framework による API 化
* React などのフロントエンド分離構成
* Docker 化、および AWS デプロイ
* 権限管理・通知機能の追加

---

## ライセンス

このプロジェクトは学習目的で作成した PoC です。
ライセンスは設定していません（無断での再利用・配布は不可）。

---

