
---

# Task Manager (PoC)

本リポジトリは、Django 5.2 を用いたタスク管理アプリケーションの **Proof of Concept (PoC)** 実装です。
タスクの CRUD 操作、検索・フィルタ機能、親子タスク構造、管理画面対応までを網羅しています。

---

## 前提条件

* Python 3.12, pip, venv
* Windows11 / WSL / Ubuntu 24.04
* VSCode

### Django インストール

```bash
pip install Django==5.2.5
```

### 型チェック・テスト関連

```bash
pip install mypy pytest pytest-django django-stubs django-stubs-ext
```

### gettext (i18n 用)

* macOS: `brew install gettext`
* Ubuntu / Debian: `sudo apt install gettext`
* Windows: [gettext for Windows](https://mlocati.github.io/articles/gettext-iconv-windows.html) をインストールし PATH に追加

---

## 主な機能

* **タスク管理（CRUD）**

  * タイトル、説明、作成日、更新日、完了状態、完了コメント、アーカイブ状態
  * 親子タスク構造を保持

* **タスク一覧 / 詳細ページ**

  * トップレベルタスクのみを一覧表示（子タスクは詳細ページで確認）
  * 検索・フィルタ：完了状態、アーカイブ状態、タイトル・コメント部分一致

* **Django 管理画面**

  * 完了状態を「完了 / 未完了」で表示
  * 検索・フィルタ対応

* **ユーザー管理**

  * Django 標準認証
  * ユーザーごとのタスク表示・操作が可能

* **API 機能（開発中）**

  1. **条件指定フォーム連携ビュー**
     フォーム入力 → 検索条件 → HTML テーブル + JSON 表示
  2. **JSON 専用 API**
     クライアント（Ajax / React / TypeScript）から直接利用可能

  * 今後、認証・認可、Pagination、Filtering 等を追加予定

* **ユニットテスト**

  * モデル・フォーム・ビュー・URL を網羅

---

## TypeScript 環境（PoC）

* `assets/ts/hello.ts` を作成
* TypeScript → JavaScript へコンパイル

  ```bash
  tsc assets/ts/hello.ts --outDir static/js --sourceMap
  ```
* VSCode で `hello.js` をデバッグ可能（ブレークポイント利用）
* 実行例：

  ```bash
  /usr/bin/node ./task_manager/static/js/hello.js
  Hello, Alice!
  Hello, Bob! You are a Engineer.
  ```

---

## 技術スタック

* Python 3.12
* Django 5.2
* SQLite3（開発環境用）
* Bootstrap 5.3
* pytest + pytest-django
* mypy 型チェック
* gettext i18n
* TypeScript（PoC）

---

## セットアップ手順

1. リポジトリのクローン

```bash
git clone https://github.com/<your-username>/task_manager.git
cd task_manager
```

2. 仮想環境の作成と有効化

```bash
python -m venv .venv
source .venv/bin/activate
```

3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

4. Django マイグレーション

```bash
python manage.py migrate
```

5. 管理ユーザー作成

```bash
python manage.py createsuperuser
```

6. 開発サーバー起動

```bash
python manage.py runserver
```

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## mypy 型チェック

```ini
[mypy]
python_version = 3.12
warn_unused_configs = True
ignore_missing_imports = True
strict = True

[mypy.plugins.django-stubs]
django_settings_module = "task_manager.settings"
```

実行例：

```bash
mypy task_manager/tasks/
```

---

## pytest 設定

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

## ディレクトリ構成（抜粋）

```bash
.
├── README.md
├── requirements.txt
├── manage.py
├── assets/ts/hello.ts
├── static/js/hello.js
├── static/js/hello.js.map
├── task_manager/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── views.py
│   └── templates/accounts/login.html
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   └── templates/tasks/task_list.html
└── templates/base.html
```

---

## 今後の展望

* フロント分離（React + TypeScript）との連携強化
* API の機能拡張（認証・認可、Pagination、Filtering 等）
* Docker 化、および AWS デプロイ
* 権限管理・通知機能の追加
* 親子タスクのネスト構造の強化

---

## ライセンス

学習目的の PoC。無断再利用・配布不可。

---


