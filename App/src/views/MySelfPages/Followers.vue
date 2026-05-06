<template>
    <div class="followers-page">
        <PageNavBar title="我的粉丝" />
        <div class="user-list">
            <UserListItem v-for="user in followersList" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" follow-text="回关" @toggle="followBack(user.user_id)" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { showToast } from 'vant'
import PageNavBar from '@/components/PageNavBar.vue'
import UserListItem from '@/components/UserListItem.vue'
const followersList = ref([
    { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'Python开发者', is_followed: false },
    { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'Vue3爱好者', is_followed: false }
])
const followBack = (userId) => { const user = followersList.value.find(u => u.user_id === userId); if (user) { user.is_followed = true; showToast('已关注') } }
</script>

<style scoped>
.followers-page { background: #f5f5f5; min-height: 100vh; }
.user-list { padding: 12px; }
</style>
