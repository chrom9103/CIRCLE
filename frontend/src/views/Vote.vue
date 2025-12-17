<script setup>
import { onMounted, ref, computed } from 'vue';
import { supabase } from '../supabase';
import { useRouter } from 'vue-router';
import { BACKEND } from '../runtimeConfig';

const router = useRouter();
const API_BASE = BACKEND;

const user = ref(null);
const loading = ref(true);
const submitting = ref(false);
const error = ref('');
const successMessage = ref('');

// 投票状態
const isMember = ref(false);
const hasVoted = ref(false);
const periodStatus = ref(null);

// 投票期間の状態
const isVotingOpen = computed(() => periodStatus.value?.status === 'open');
const isBeforeVoting = computed(() => periodStatus.value?.status === 'before');
const isAfterVoting = computed(() => periodStatus.value?.status === 'after');

// 投票可能かどうか
const canVote = computed(() => {
    return user.value && isMember.value && !hasVoted.value && isVotingOpen.value;
});

async function getUser() {
    const { data, error: userError } = await supabase.auth.getUser();
    if (userError) {
        console.error('Error fetching user:', userError.message);
        return null;
    }
    return data.user;
}

async function getAccessToken() {
    const { data } = await supabase.auth.getSession();
    return data.session?.access_token || null;
}

async function fetchVoteStatus() {
    const token = await getAccessToken();
    if (!token) {
        error.value = 'ログインが必要です';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/vote/status`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || '投票状態の取得に失敗しました');
        }

        const data = await response.json();
        isMember.value = data.is_member;
        hasVoted.value = data.has_voted;
        periodStatus.value = data.period;
    } catch (e) {
        error.value = e.message;
    }
}

async function submitVote(vote) {
    if (submitting.value) return;
    
    const voteLabel = vote ? '賛成' : '反対';
    const confirmMessage = `「${voteLabel}」に投票します。\n\n※一度投票すると変更できません。よろしいですか？`;
    
    if (!confirm(confirmMessage)) {
        return;
    }

    submitting.value = true;
    error.value = '';
    successMessage.value = '';

    const token = await getAccessToken();
    if (!token) {
        error.value = 'ログインが必要です';
        submitting.value = false;
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/vote`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ vote })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || '投票に失敗しました');
        }

        successMessage.value = data.message;
        hasVoted.value = true;
    } catch (e) {
        error.value = e.message;
    } finally {
        submitting.value = false;
    }
}

function formatDate(isoString) {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'Asia/Tokyo'
    });
}

onMounted(async () => {
    loading.value = true;
    user.value = await getUser();
    
    if (user.value) {
        await fetchVoteStatus();
    }
    
    loading.value = false;
});
</script>

<template>
    <div class="vote-container">
        <h1>団体名称変更に関する投票</h1>
        
        <!-- ローディング -->
        <div v-if="loading" class="loading">
            <p>読み込み中...</p>
        </div>

        <!-- 未ログイン -->
        <div v-else-if="!user" class="not-logged-in">
            <p>投票するにはログインが必要です。</p>
            <router-link to="/signin" class="btn btn-primary">ログイン</router-link>
        </div>

        <!-- ログイン済み -->
        <div v-else class="vote-content">
            <!-- 投票期間情報 -->
            <div class="period-info" v-if="periodStatus">
                <p class="period-label">投票期間:</p>
                <p class="period-dates">
                    {{ formatDate(periodStatus.start) }} ～ {{ formatDate(periodStatus.end) }}
                </p>
                <p :class="['period-status', periodStatus.status]">
                    {{ periodStatus.message }}
                </p>
            </div>

            <!-- メンバーでない場合 -->
            <div v-if="!isMember" class="not-member">
                <p class="warning">⚠️ メンバー権限がないため投票できません。</p>
            </div>

            <!-- 投票内容 -->
            <div class="vote-proposal" v-if="isMember">
                <h2>投票内容</h2>
                <div class="proposal-box">
                    <p class="proposal-main">
                        「PiedPiper青山テック愛好会は団体名を改称するべきである。」
                    </p>
                    <p class="proposal-sub">
                        付帯文: 改称後の名称を「Digitart デジタル創作愛好会」とする
                    </p>
                </div>
            </div>

            <!-- エラーメッセージ -->
            <div v-if="error" class="error-message">
                <p>{{ error }}</p>
            </div>

            <!-- 成功メッセージ -->
            <div v-if="successMessage" class="success-message">
                <p>✅ {{ successMessage }}</p>
            </div>

            <!-- 投票済み -->
            <div v-if="hasVoted && isMember" class="already-voted">
                <p>✅ 投票済みです。ご協力ありがとうございました。</p>
                <p class="note">※投票内容の変更はできません。</p>
            </div>

            <!-- 投票期間前 -->
            <div v-else-if="isBeforeVoting && isMember" class="before-voting">
                <p>投票期間開始までお待ちください。</p>
            </div>

            <!-- 投票期間終了 -->
            <div v-else-if="isAfterVoting && isMember" class="after-voting">
                <p>投票期間は終了しました。</p>
            </div>

            <!-- 投票ボタン -->
            <div v-else-if="canVote" class="vote-buttons">
                <h3>上記の提案に対して投票してください</h3>
                <div class="buttons">
                    <button 
                        @click="submitVote(true)" 
                        :disabled="submitting"
                        class="btn btn-agree"
                    >
                        {{ submitting ? '送信中...' : '賛成' }}
                    </button>
                    <button 
                        @click="submitVote(false)" 
                        :disabled="submitting"
                        class="btn btn-disagree"
                    >
                        {{ submitting ? '送信中...' : '反対' }}
                    </button>
                </div>
                <p class="vote-warning">⚠️ 一度投票すると変更できません</p>
            </div>
        </div>

        <!-- 戻るリンク -->
        <div class="back-link">
            <router-link to="/dashboard">ダッシュボードに戻る</router-link>
        </div>
    </div>
</template>

<style scoped>
.vote-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    text-align: center;
    margin-bottom: 2rem;
    color: #333;
}

.loading {
    text-align: center;
    padding: 2rem;
}

.not-logged-in {
    text-align: center;
    padding: 2rem;
}

.period-info {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.period-label {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.period-dates {
    color: #666;
    margin-bottom: 0.5rem;
}

.period-status {
    font-weight: bold;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
}

.period-status.before {
    background: #fff3cd;
    color: #856404;
}

.period-status.open {
    background: #d4edda;
    color: #155724;
}

.period-status.after {
    background: #f8d7da;
    color: #721c24;
}

.not-member {
    text-align: center;
    padding: 1rem;
}

.warning {
    color: #856404;
    background: #fff3cd;
    padding: 1rem;
    border-radius: 8px;
}

.vote-proposal {
    margin-bottom: 2rem;
}

.vote-proposal h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
}

.proposal-box {
    background: #f7f7f7;
    border: 2px solid #b3b3b3;
    border-radius: 8px;
    padding: 1.5rem;
}

.proposal-main {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #1d1d1d;
}

.proposal-sub {
    color: #666;
    font-size: 0.95rem;
    padding-left: 1rem;
}

.error-message {
    background: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.success-message {
    background: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.already-voted, .before-voting, .after-voting {
    text-align: center;
    padding: 1.5rem;
    background: #f5f5f5;
    border-radius: 8px;
}

.already-voted .note {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.5rem;
}

.vote-buttons {
    text-align: center;
}

.vote-buttons h3 {
    font-size: 1rem;
    margin-bottom: 1.5rem;
    color: #333;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1rem;
}

.btn {
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: #2196f3;
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: #1976d2;
}

.btn-agree {
    background: #4caf50;
    color: white;
    min-width: 120px;
}

.btn-agree:hover:not(:disabled) {
    background: #388e3c;
}

.btn-disagree {
    background: #f44336;
    color: white;
    min-width: 120px;
}

.btn-disagree:hover:not(:disabled) {
    background: #d32f2f;
}

.vote-warning {
    color: #856404;
    font-size: 0.9rem;
    margin-top: 1rem;
}

.back-link {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
}

.back-link a {
    color: #2196f3;
    text-decoration: none;
}

.back-link a:hover {
    text-decoration: underline;
}
</style>
