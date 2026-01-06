<<<<<<< HEAD
export const RUNTIME = (typeof window !== 'undefined' && (window as any).__APP_ENV__ && (window as any).__APP_ENV__.VITE_SUPABASE_URL)
	? (window as any).__APP_ENV__
	: import.meta.env
export const BACKEND = RUNTIME.VITE_API_BASE_URL ?? ''
=======
// ビルド時に埋め込まれた環境変数を使用（env.jsによる公開を廃止）
export const RUNTIME = import.meta.env

const rawApiBase = RUNTIME.VITE_API_BASE_URL ?? ''
export const BACKEND = (typeof rawApiBase === 'string') ? rawApiBase.replace(/^"(.*)"$/, '$1') : ''
>>>>>>> 71c69100e9f513d944ec1670a04eb0f291b0adff
