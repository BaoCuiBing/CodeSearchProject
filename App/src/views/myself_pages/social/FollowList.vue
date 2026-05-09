<template>
    <div class="follow-list-page">
        <PageNavBar :title="title" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <div v-else class="user-list">
            <van-empty v-if="users.length === 0" description="暂无用户" />
            <UserListItem v-for="user in users" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" @toggle="toggleFollow(user)" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from 'vant'
import PageNavBar from '@/components/PageNavBar.vue'
import UserListItem from '@/components/UserListItem.vue'
import { followApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
const route = useRoute()
const type = route.query.type || 'following'
const title = type === 'following' ? '我的关注' : '我的粉丝'
const loading = ref(true)
const error = ref('')
const users = ref([])
const loadUsers = async () => {
    loading.value = true
    error.value = ''
    try {
        const userId = getUserId()
        let data
        if (type === 'following') {
            data = await followApi.getFollowing(userId)
        } else {
            data = await followApi.getFollowers(userId)
        }
        users.value = (data.list || []).map(u => ({ ...u, is_followed: u.is_mutual || u.is_followed_back || false }))
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const toggleFollow = async (user) => {
    try {
        await followApi.toggleFollow(user.user_id)
        user.is_followed = !user.is_followed
        showToast(user.is_followed ? '已关注' : '已取消关注')
    } catch (err) {
        showToast(err.message || '操作失败')
    }
}
loadUsers()
</script>

<style scoped>
.follow-list-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.user-list { padding: 12px; }
</style>