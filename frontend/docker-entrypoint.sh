#!/bin/sh
set -e

HTML_FILE="/usr/share/nginx/html/CIRCLE/index.html"

# Build inline script with only PUBLIC environment variables
# Note: SUPABASE_SERVICE_ROLE_KEY, DISCORD_BOT_TOKEN etc. are SECRET and should NOT be exposed to frontend

if [ -f "$HTML_FILE" ]; then
  # Replace the entire placeholder with actual environment values
  sed -i "s|window.__APP_ENV__=window.__APP_ENV__||{}|window.__APP_ENV__={VITE_SUPABASE_URL:\"${VITE_SUPABASE_URL:-}\",VITE_SUPABASE_ANON_KEY:\"${VITE_SUPABASE_ANON_KEY:-}\",VITE_API_BASE_URL:\"${VITE_API_BASE_URL:-}\"}|g" "$HTML_FILE"
fi

exec nginx -g 'daemon off;'
