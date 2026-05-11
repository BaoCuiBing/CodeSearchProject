<template>
    <div class="myself-page">
        <van-nav-bar title="我的" fixed placeholder />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <div v-else class="user-header">
            <div class="user-info">
                <van-image round width="64px" height="64px" :src="user?.avatar || ''" />
                <div class="user-meta">
                    <h3 v-if="user" @click="goToProfile">{{ user.username }}</h3>
                    <h3 v-else class="login-text" @click="goToLogin">登录</h3>
                    <p class="user-bio">{{ user?.bio || '这个人很懒，什么都没写' }}</p>
                </div>
                <van-icon name="setting-o" size="24" color="#999" @click="goToSettings" />
            </div>
            <div class="user-stats">
                <div class="stat-item" @click="goToFollowing">
                    <span class="stat-num">{{ user?.stats?.following_count || 0 }}</span>
                    <span class="stat-label">关注</span>
                </div>
                <div class="stat-item" @click="goToFollowers">
                    <span class="stat-num">{{ user?.stats?.follower_count || 0 }}</span>
                    <span class="stat-label">粉丝</span>
                </div>
                <div class="stat-item">
                    <span class="stat-num">{{ user?.stats?.like_count || 0 }}</span>
                    <span class="stat-label">获赞</span>
                </div>
            </div>
        </div>
        <div class="menu-section">
            <van-cell-group>
                <van-cell title="我的文章" icon="notes-o" is-link @click="goToMyArticles" />
                <van-cell title="我的问题" icon="question-o" is-link @click="goToMyQuestions" />
                <van-cell title="我的收藏" icon="star-o" is-link @click="goToFavorites" />
            </van-cell-group>
        </div>
        <div class="menu-section">
            <van-cell-group>
                <van-cell title="个人资料" icon="user-o" is-link @click="goToProfile" />
                <van-cell title="账号与安全" icon="shield-o" is-link @click="goToSecurity" />
                <van-cell title="关于我们" icon="info-o" is-link @click="goToAbout" />
            </van-cell-group>
        </div>
        <div v-if="isLogin()" class="menu-section">
            <van-button block type="danger" class="logout-btn" @click="handleLogout">退出登录</van-button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog } from 'vant'
import { profileApi } from '@/assets/app_request_api.js'
import { getUserId, isLogin, logout as clearUser } from '@/assets/local_storage.js'
const router = useRouter()
const loading = ref(true)
const error = ref('')
const user = ref(null)
const loadUserProfile = async () => {
    if (!isLogin()) { loading.value = false; return }
    loading.value = true
    error.value = ''
    try {
        const data = await profileApi.getProfile(getUserId())
        user.value = data
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const goToSettings = () => { router.push('/settings') }
const goToFollowing = () => { router.push('/following') }
const goToFollowers = () => { router.push('/followers') }
const goToMyArticles = () => { router.push('/my-articles') }
const goToMyQuestions = () => { router.push('/my-questions') }
const goToFavorites = () => { router.push('/my-favorites') }
const goToProfile = () => { router.push('/profile') }
const goToSecurity = () => { router.push('/security') }
const goToAbout = () => { router.push('/about') }
const goToLogin = () => { router.push('/login') }
const handleLogout = () => {
    showConfirmDialog({ title: '确认退出', message: '确定要退出登录吗？' }).then(() => { clearUser(); user.value = null; error.value = ''; router.replace('/shouye') }).catch(() => {})
}
onMounted(() => { loadUserProfile() })
</script>

<style scoped>
.myself-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.user-header { background: #fff; padding: 24px 16px; margin-bottom: 8px; }
.user-info { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.user-meta { flex: 1; }
.user-meta h3 { margin: 0 0 8px; font-size: 20px; color: #333; }
.login-text { color: #1989fa; cursor: pointer; }
.user-meta p { margin: 0; font-size: 14px; color: #999; }
.user-bio { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; }
.user-stats { display: flex; justify-content: space-around; }
.stat-item { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.stat-num { font-size: 20px; font-weight: 600; color: #333; }
.stat-label { font-size: 13px; color: #999; }
.menu-section { margin-bottom: 8px; }
.menu-section .van-cell { padding-left: 16px; }
.menu-section .van-cell__title { letter-spacing: 1px; }
.logout-btn { margin: 0 16px; width: calc(100% - 32px); }
.bottom-spacer { height: 80px; }
</style>
