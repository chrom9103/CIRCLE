import { createClient } from '@supabase/supabase-js'

function getRuntimeEnv() {
	if (typeof window !== 'undefined' && (window as any).__APP_ENV__ && (window as any).__APP_ENV__.VITE_SUPABASE_URL) {
		return (window as any).__APP_ENV__
	}
	return import.meta.env
}

const runtimeEnv = getRuntimeEnv()
const supabaseUrl = runtimeEnv.VITE_SUPABASE_URL
const supabaseAnonKey = runtimeEnv.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl) {
	throw new Error('supabaseUrl is required. Check build-time VITE_SUPABASE_URL')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
