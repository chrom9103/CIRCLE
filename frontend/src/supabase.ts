import { createClient } from '@supabase/supabase-js'

// ビルド時に埋め込まれた環境変数を使用（env.jsによる公開を廃止）
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl) {
	throw new Error('supabaseUrl is required. Check build-time VITE_SUPABASE_URL')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
