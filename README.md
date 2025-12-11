# CIRCLE_PiedPiper-Hackathon

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
 # CIRCLE — PiedPiper 会計管理システム

このリポジトリは PiedPiper（青山テック愛好会）向けの会計管理システムです。
フロントエンドは Vue 3 + Vite、バックエンドは FastAPI（Python）で構成され、Discord サインインや Supabase を用いた認証／データ永続化を想定しています。

目次
- 概要
- アーキテクチャと使用技術
- ローカル開発手順（frontend / backend）
- 環境変数
- Docker / コンテナについて
- 主要ファイルとディレクトリ
- 貢献と連絡先

## 概要

このプロジェクトは次の機能を持ちます（実装済／設計中の機能を含む）:
- Discord OAuth によるサインイン
- 会計レコードの作成・閲覧・ステータス管理（未清算／清算済み／削除など）
- 管理者向けのレコード管理 UI（同期・フィルタ・操作）
- バックグラウンドでの Discord と Supabase の同期（管理者リスト / メンバーリスト）

## アーキテクチャと使用技術

- フロントエンド: Vue 3（Composition API） + Vite + TypeScript 設定ファイルあり
  - UI はコンポーネント化（`src/components`）、状態は Pinia や Supabase クライアントで管理
- バックエンド: Python + FastAPI
  - API ルータは `backend/routers`、DB 操作ロジックは `backend/cruds` に配置
  - オプションで discord.py を用いた Discord クライアント連携（`backend/cruds/discord_sync.py` など）
- 認証 / DB: Supabase（Postgres）を想定
- 開発環境: Docker Compose（`docker-compose.yaml` / `docker-compose.override.yaml`）

## ローカル開発手順

前提:
- Node.js（推奨: 18+）と Python（3.10+ 推奨）、Docker（任意）がインストールされていること。

1) フロントエンド

```powershell
cd frontend
npm install
npm run dev
```

2) バックエンド

推奨: 仮想環境を作成してから依存をインストールします。

```powershell
cd backend
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1   # PowerShell の場合
pip install -r requirements.txt
uvicorn main:app --reload
```

バックエンドは `main.py` の起動時に Discord 連携モジュールをオプションで読み込みます（discord ライブラリが環境に無い場合は無効化されます）。

### Docker（オプション）

このリポジトリには `docker-compose.yaml` が含まれており、フロント / バックエンドと DB をまとめて起動できます。設定に従ってイメージをビルドしてください。

```powershell
docker compose build
docker compose up
```

（初回起動時は依存の再インストールや環境変数の設定が必要です）

## 環境変数

プロジェクトで使用する主な env 変数（例）:

- フロントエンド（`.env` / Vite）
  - `VITE_API_BASE_URL` — バックエンド API のベース URL

- バックエンド（例: `.env` やコンテナの環境）
  - `DATABASE_URL` — PostgreSQL 接続文字列 (Supabase の場合は Supabase の接続文字列)
  - `DISCORD_BOT_TOKEN` — （任意）discord.py を使う場合のボットトークン
  - `SUPABASE_URL`, `SUPABASE_KEY` — Supabase クライアント用

実際のキーやシークレットはソース管理に含めないでください。

## 主要ファイルとディレクトリ

- `frontend/` — Vue アプリケーション
  - `src/components` — UI コンポーネント（管理用コンポーネントは `src/components/admin`）
  - `src/views` — ルーティング用ビュー
  - `vite.config.ts`, `package.json`
- `backend/` — FastAPI アプリケーション
  - `main.py` — アプリ起動点
  - `routers/` — API ルータ
  - `cruds/` — DB 操作 / 外部同期ロジック（Discord 同期等）
  - `requirements.txt`
- `docker-compose.yaml`, `docker-compose.override.yaml` — 開発/デプロイ用 compose 設定

## 開発のヒント

- フロントで `node_modules` が無い場合、TypeScript/Vue の言語サーバがエラーを表示することがあります。`npm install` を行ってからエディタの再起動（または Vue/TypeScript サーバの再起動）を実行してください。
- バックエンドに discord 機能を追加する際は `discord.py` の依存を `requirements.txt` に加えてからコンテナを再ビルドしてください。起動時に optional import を行っているため、discord が無くても通常の API 動作は行えます。

## 貢献

バグ報告・機能要望は issue へお願いします。Pull Request は小さな単位で、関連する説明と動作確認手順を添えてください。

