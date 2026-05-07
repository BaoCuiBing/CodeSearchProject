<template>
    <div class="followers-page">
        <PageNavBar title="我的粉丝" />
        <div class="user-list">
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
const followersList = ref([])
const loadFollowers = async () => {
    const data = await followApi.getFollowers(getUserId(), 1, 20)
    followersList.value = data?.list || []
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
.user-list { padding: 12px; }
</style>
