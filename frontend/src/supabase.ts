import { createClient } from '@supabase/supabase-js'

<<<<<<< HEAD
function getRuntimeEnv() {
	if (typeof window !== 'undefined' && (window as any).__APP_ENV__ && (window as any).__APP_ENV__.VITE_SUPABASE_URL) {
		return (window as any).__APP_ENV__
	}
	return import.meta.env
}

const runtimeEnv = getRuntimeEnv()
const supabaseUrl = runtimeEnv.VITE_SUPABASE_URL
const supabaseAnonKey = runtimeEnv.VITE_SUPABASE_ANON_KEY
=======
// ビルド時に埋め込まれた環境変数を使用（env.jsによる公開を廃止）
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY
>>>>>>> 71c69100e9f513d944ec1670a04eb0f291b0adff

if (!supabaseUrl) {
	throw new Error('supabaseUrl is required. Check build-time VITE_SUPABASE_URL')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
