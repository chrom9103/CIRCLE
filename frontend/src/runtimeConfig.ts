// Prefer runtime-injected `window.__APP_ENV__` when it contains a supabase URL,
// otherwise fall back to `import.meta.env` for build-time variables.
export const RUNTIME = (typeof window !== 'undefined' && (window as any).__APP_ENV__ && (window as any).__APP_ENV__.VITE_SUPABASE_URL)
	? (window as any).__APP_ENV__
	: import.meta.env

// Normalize BACKEND value similar to remote changes
const rawApiBase = RUNTIME.VITE_API_BASE_URL ?? ''
export const BACKEND = (typeof rawApiBase === 'string') ? rawApiBase.replace(/^"(.*)"$/, '$1') : ''
