<template>
    <div class="follow-list-page">
        <PageNavBar :title="title" />
        <div class="user-list">
            <van-empty v-if="users.length === 0" description="暂无用户" />
            <UserListItem v-for="user in users" :key="user.user_id" :avatar="user.avatar" :username="user.username" :bio="user.bio" :is-followed="user.is_followed" @toggle="toggleFollow(user)" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import UserListItem from '@/components/UserListItem.vue'
const route = useRoute()
const type = route.query.type || 'following'
const title = type === 'following' ? '我的关注' : '我的粉丝'
const users = ref([
    { user_id: 1, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '前端开发工程师', is_followed: true },
    { user_id: 2, username: 'DBA老张', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '数据库管理员', is_followed: true },
    { user_id: 3, username: '运维小李', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'DevOps 工程师', is_followed: false },
    { user_id: 4, username: 'AI大牛', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '人工智能研究员', is_followed: true }
])
const toggleFollow = (user) => { user.is_followed = !user.is_followed }
</script>

<style scoped>
.follow-list-page { background: #f5f5f5; min-height: 100vh; }
.user-list { padding: 12px; }
</style>
