#!/bin/sh
set -e

TEMPLATE="/usr/share/nginx/html/CIRCLE/env.template.js"
OUT="/usr/share/nginx/html/CIRCLE/env.js"

if [ -f "$TEMPLATE" ]; then
  sed -e "s|__VITE_SUPABASE_URL__|${VITE_SUPABASE_URL:-}|g" \
      -e "s|__VITE_SUPABASE_ANON_KEY__|${VITE_SUPABASE_ANON_KEY:-}|g" \
      -e "s|__VITE_API_BASE_URL__|${VITE_API_BASE_URL:-}|g" \
      -e "s|__SUPABASE_SERVICE_ROLE_KEY__|${SUPABASE_SERVICE_ROLE_KEY:-}|g" \
      -e "s|__DISCORD_BOT_TOKEN__|${DISCORD_BOT_TOKEN:-}|g" \
      -e "s|__DISCORD_GUILD_ID__|${DISCORD_GUILD_ID:-}|g" \
      -e "s|__DISCORD_ROLE_ID_ADMIN__|${DISCORD_ROLE_ID_ADMIN:-}|g" \
      -e "s|__DISCORD_ROLE_ID_MEMBER__|${DISCORD_ROLE_ID_MEMBER:-}|g" \
      "$TEMPLATE" > "$OUT"
fi

exec nginx -g 'daemon off;'
