<template>
    <div class="following-page">
        <PageNavBar title="我的关注" />
        <div class="user-list">
            <van-empty v-if="followingList.length === 0" description="暂无关注" />
            <UserListItem v-for="user in followingList" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" plain @toggle="unfollow(user.user_id)" />
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
const followingList = ref([])
const loadFollowing = async () => {
    const data = await followApi.getFollowing(getUserId(), 1, 20)
    followingList.value = data?.list || []
}
const unfollow = async (userId) => {
    await followApi.toggleFollow(userId)
    followingList.value = followingList.value.filter(u => u.user_id !== userId)
    showToast('已取消关注')
}
onMounted(() => { loadFollowing() })
</script>

<style scoped>
.following-page { background: #f5f5f5; min-height: 100vh; }
.user-list { padding: 12px; }
</style>
