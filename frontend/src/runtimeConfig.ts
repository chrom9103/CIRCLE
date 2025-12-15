export const RUNTIME = (typeof window !== 'undefined' && (window as any).__APP_ENV__) ? (window as any).__APP_ENV__ : import.meta.env
export const BACKEND = RUNTIME.VITE_API_BASE_URL ?? ''
