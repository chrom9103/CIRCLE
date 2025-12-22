// ビルド時に埋め込まれた環境変数を使用（env.jsによる公開を廃止）
export const RUNTIME = import.meta.env

const rawApiBase = RUNTIME.VITE_API_BASE_URL ?? ''
export const BACKEND = (typeof rawApiBase === 'string') ? rawApiBase.replace(/^"(.*)"$/, '$1') : ''
