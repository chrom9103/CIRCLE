const getRuntime = () => {
	if (typeof window !== 'undefined' && (window as any).__APP_ENV__ && Object.keys((window as any).__APP_ENV__).length > 0) {
		return (window as any).__APP_ENV__
	}
	return import.meta.env
}

export const RUNTIME = getRuntime()

const rawApiBase = RUNTIME.VITE_API_BASE_URL ?? ''
export const BACKEND = (typeof rawApiBase === 'string') ? rawApiBase.replace(/^"(.*)"$/, '$1') : ''
