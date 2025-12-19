#!/bin/sh
set -e

# Generate a small JS file that exposes only public runtime env vars to the SPA
# Write directly to env.js to avoid fragile sed expressions and quoting issues.
OUT_FILE="/usr/share/nginx/html/CIRCLE/env.js"

cat > "$OUT_FILE" <<-EOF
window.__APP_ENV__ = {
  VITE_SUPABASE_URL: "${VITE_SUPABASE_URL:-}",
  VITE_SUPABASE_ANON_KEY: "${VITE_SUPABASE_ANON_KEY:-}",
  VITE_API_BASE_URL: "${VITE_API_BASE_URL:-}"
};
EOF

# Ensure the SPA loads the runtime env script before the main bundle
INDEX_FILE="/usr/share/nginx/html/CIRCLE/index.html"
ENV_SCRIPT_TAG='<script src="/CIRCLE/env.js"></script>'
if [ -f "$INDEX_FILE" ]; then
  if ! grep -qF "$ENV_SCRIPT_TAG" "$INDEX_FILE"; then
    # 1) Preferred: insert after placeholder script that ensures window.__APP_ENV__ exists
    if grep -qF 'window.__APP_ENV__=window.__APP_ENV__||{}' "$INDEX_FILE"; then
      awk -v tag="$ENV_SCRIPT_TAG" '{
        print
        if (!done && $0 ~ /window.__APP_ENV__=window.__APP_ENV__\|\|\{\}/) { print tag; done=1 }
      }' "$INDEX_FILE" > "${INDEX_FILE}.tmp" && mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
    else
      # 2) Fallback A: insert before the first script tag that likely loads the app bundle
      if awk '/<script[^>]*type="module"[^>]*>/ {exit 0} END{exit 1}' "$INDEX_FILE" >/dev/null 2>&1; then
        awk -v tag="$ENV_SCRIPT_TAG" '{ if(!done && $0 ~ /<script[^>]*type="module"/){ print tag; done=1 } print }' "$INDEX_FILE" > "${INDEX_FILE}.tmp" && mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
      elif awk '/<script[^>]*src=[^>]*\.js/ {exit 0} END{exit 1}' "$INDEX_FILE" >/dev/null 2>&1; then
        awk -v tag="$ENV_SCRIPT_TAG" '{ if(!done && $0 ~ /<script[^>]*src=[^>]*\.js/){ print tag; done=1 } print }' "$INDEX_FILE" > "${INDEX_FILE}.tmp" && mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
      else
        # 3) Final fallback: insert before closing </head>
        awk -v tag="$ENV_SCRIPT_TAG" '{ if(!done && $0 ~ /<\/head>/){ print tag; done=1 } print }' "$INDEX_FILE" > "${INDEX_FILE}.tmp" && mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
      fi
    fi
  fi
fi

exec nginx -g 'daemon off;'
