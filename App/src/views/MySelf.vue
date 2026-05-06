<template>
    <div class="myself-page">
        <van-nav-bar title="我的" fixed placeholder />
        <div class="user-header">
            <div class="user-info">
                <van-image round width="64px" height="64px" :src="user.avatar" />
                <div class="user-meta">
                    <h3>{{ user.username }}</h3>
                    <p>{{ user.bio || '这个人很懒，什么都没写' }}</p>
                </div>
                <van-icon name="setting-o" size="24" color="#999" @click="goToSettings" />
            </div>
            <div class="user-stats">
                <div class="stat-item" @click="goToFollowing">
                    <span class="stat-num">{{ user.stats.following_count }}</span>
                    <span class="stat-label">关注</span>
                </div>
                <div class="stat-item" @click="goToFollowers">
                    <span class="stat-num">{{ user.stats.follower_count }}</span>
                    <span class="stat-label">粉丝</span>
                </div>
                <div class="stat-item">
                    <span class="stat-num">{{ user.stats.like_count }}</span>
                    <span class="stat-label">获赞</span>
                </div>
            </div>
        </div>
        <div class="menu-section">
            <van-cell-group>
                <van-cell title="我的文章" icon="notes-o" is-link @click="goToMyArticles" />
                <van-cell title="我的问题" icon="question-o" is-link @click="goToMyQuestions" />
                <van-cell title="我的收藏" icon="star-o" is-link @click="goToFavorites" />
                <van-cell title="浏览历史" icon="clock-o" is-link @click="goToHistory" />
            </van-cell-group>
        </div>
        <div class="menu-section">
            <van-cell-group>
                <van-cell title="个人资料" icon="user-o" is-link @click="goToProfile" />
                <van-cell title="账号与安全" icon="shield-o" is-link @click="goToSecurity" />
                <van-cell title="关于我们" icon="info-o" is-link @click="goToAbout" />
            </van-cell-group>
        </div>
        <div class="bottom-spacer"></div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const user = ref({
    user_id: 1,
    username: '程序员小明',
    avatar: 'https://img.yzcdn.cn/vant/cat.jpeg',
    bio: '热爱编程，乐于分享',
    email: 'xiaoming@example.com',
    location: '北京',
    website: 'https://xiaoming.dev',
    github: 'https://github.com/xiaoming',
    stats: { article_count: 56, question_count: 12, follower_count: 256, following_count: 128, like_count: 1024, view_count: 15678 },
    created_at: '2024-01-01 10:00:00'
})
const goToSettings = () => { router.push('/settings') }
const goToFollowing = () => { router.push('/following') }
const goToFollowers = () => { router.push('/followers') }
const goToMyArticles = () => { router.push('/my-articles') }
const goToMyQuestions = () => { router.push('/my-questions') }
const goToFavorites = () => { router.push('/favorites') }
const goToHistory = () => { router.push('/history') }
const goToProfile = () => { router.push('/profile') }
const goToSecurity = () => { router.push('/security') }
const goToAbout = () => { router.push('/about') }
</script>

<style scoped>
.myself-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.user-header { background: #fff; padding: 24px 16px; margin-bottom: 8px; }
.user-info { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.user-meta { flex: 1; }
.user-meta h3 { margin: 0 0 8px; font-size: 20px; color: #333; }
.user-meta p { margin: 0; font-size: 14px; color: #999; }
.user-stats { display: flex; justify-content: space-around; }
.stat-item { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.stat-num { font-size: 20px; font-weight: 600; color: #333; }
.stat-label { font-size: 13px; color: #999; }
.menu-section { margin-bottom: 8px; }
.menu-section .van-cell { padding-left: 16px; }
.menu-section .van-cell__title { letter-spacing: 1px; }
.bottom-spacer { height: 80px; }
</style>
