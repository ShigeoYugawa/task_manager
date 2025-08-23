
---

# Task Manager (PoC)

本リポジトリは、Django 5.2 を用いたタスク管理アプリケーションの **Proof of Concept (PoC)** 実装です。
小規模ながら、タスクの CRUD 操作、検索・フィルタ機能、管理画面対応まで網羅しており、今後の拡張や API 化のベースとして利用できます。

---

## 主な機能

* タスク管理（CRUD）

  * タイトル、説明、作成日、更新日、完了状態、完了コメント、アーカイブ状態
* タスク一覧画面での検索・フィルタ

  * 完了状態・アーカイブ状態の絞り込み
  * タイトル・完了コメントの部分一致検索
* 管理画面 (Django Admin) でのタスク管理

  * 完了状態を「完了 / 未完了」で表示
  * 検索・フィルタ対応
* ユニットテストでモデル・フォーム・ビュー・URL を網羅

※ ユーザー管理は Django 標準認証を使用。現時点では多ユーザー対応の画面は PoC 段階。

---

## 技術スタック

* Python 3.12
* Django 5.2
* SQLite3 (開発環境用)
* pytest + pytest-django によるユニットテスト

将来的には PostgreSQL や Docker/AWS 環境での運用を想定しています。

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
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. マイグレーションの実行

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

## ディレクトリ構成（概要）

```
task_manager/
├── manage.py
├── task_manager/       # プロジェクト設定
├── tasks/              # タスク管理アプリ
│   ├── admin.py        # 管理画面カスタマイズ
│   ├── apps.py
│   ├── forms.py        # タスク作成・検索フォーム
│   ├── models.py       # タスクモデル
│   ├── services.py     # ビジネスロジック（検索・フィルタ）
│   ├── urls.py         # URLルーティング
│   ├── views.py        # ユーザー画面用ビュー
│   ├── templates/      # テンプレート
│   │   └── tasks/
│   │       ├── task_list.html
│   │       ├── task_detail.html
│   │       ├── task_form.html
│   │       └── task_confirm_delete.html
│   └── tests/          # ユニットテスト
└── db.sqlite3          # 開発用データベース
```

---

## テストの実行

pytest でユニットテストを実行可能です：

```bash
pytest -v
```

* モデル、フォーム、ビュー、URL のテストを網羅
* CRUD 操作、検索・フィルタ機能の確認済み

---

## 今後の展望

* Django REST Framework による API 化
* React などのフロントエンド分離構成
* Docker 化、および AWS デプロイ
* 権限管理・通知機能の追加

---

## ライセンス

このプロジェクトは学習目的で作成した PoC です。
ライセンスは設定していません（無断での再利用・配布はできません）。

---

