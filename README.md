
---

# Task Manager (PoC)

本リポジトリは、Django を用いたタスク管理アプリケーションの **Proof of Concept (PoC)** 実装です。
小規模ながら、ユーザー管理とタスク管理の基本的な機能を備えており、拡張・改良のベースとして利用できます。

---

## 主な機能

* Django 標準ユーザー認証によるログイン / ログアウト
* 管理画面 (Django Admin) からのタスク管理
* タスクモデルの基本機能

  * タイトル、説明、作成日、期日、完了フラグ
* ユーザー画面（PoC段階）：タスク一覧表示、タスクの追加 / 編集 / 削除

---

## 技術スタック

* Python 3.12
* Django 5.2
* SQLite3 (開発環境用)

将来的には PostgreSQL などの本番向け DB や Docker/AWS 環境での運用を想定しています。

---

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/<your-username>/task-manager.git
cd task-manager
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
│   ├── models.py       # タスクモデル
│   ├── views.py        # ユーザー画面用ビュー
│   ├── urls.py         # URLルーティング
│   └── templates/      # テンプレート
└── db.sqlite3          # 開発用データベース
```

---

## 今後の展望

* API (Django REST Framework) の導入
* React などによるフロントエンド分離構成
* Docker 化、および AWS へのデプロイ
* 権限管理や通知機能の追加

---

## ライセンス

このプロジェクトは学習目的で作成したPoCです。  
ライセンスは設定していません（無許可での再利用・配布はできません）。

---
