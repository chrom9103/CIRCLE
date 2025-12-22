#!/bin/sh
set -e

# 環境変数はビルド時に埋め込まれるため、実行時の env.js 生成は不要
# セキュリティ上の理由により env.js による公開を廃止

exec nginx -g 'daemon off;'
