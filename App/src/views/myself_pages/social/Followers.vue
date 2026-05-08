<template>
    <div class="followers-page">
        <PageNavBar title="我的粉丝" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <div v-else-if="error" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ error }}</p>
            <van-button type="primary" size="small" @click="loadFollowers">重试</van-button>
        </div>
        <div v-else class="user-list">
            <van-empty v-if="followersList.length === 0" description="暂无粉丝" />
            <UserListItem v-for="user in followersList" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" follow-text="回关" @toggle="followBack(user.user_id)" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import { followApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
import UserListItem from '@/components/UserListItem.vue'
const loading = ref(true)
const error = ref('')
const followersList = ref([])
const loadFollowers = async () => {
    loading.value = true
    error.value = ''
    try {
        const data = await followApi.getFollowers(getUserId(), 1, 20)
        followersList.value = (data?.list || []).map(u => ({ ...u, is_followed: u.is_followed_back || false }))
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const followBack = async (userId) => {
    await followApi.toggleFollow(userId)
    const user = followersList.value.find(u => u.user_id === userId)
    if (user) { user.is_followed = true }
    showToast('已关注')
}
onMounted(() => { loadFollowers() })
</script>

<style scoped>
.followers-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.user-list { padding: 12px; }
</style>