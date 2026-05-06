<template>
    <div class="follow-list-page">
        <van-nav-bar :title="title" left-arrow @click-left="goBack" fixed placeholder />
        <div class="user-list">
            <div v-for="user in users" :key="user.user_id" class="user-item">
                <van-image round width="48px" height="48px" :src="user.avatar" />
                <div class="user-info">
                    <span class="user-name">{{ user.username }}</span>
                    <span class="user-bio">{{ user.bio }}</span>
                </div>
                <van-button size="small" :type="user.is_followed ? 'default' : 'primary'" @click="toggleFollow(user)">{{ user.is_followed ? '已关注' : '关注' }}</van-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const type = route.query.type || 'following'
const title = type === 'following' ? '我的关注' : '我的粉丝'
const users = ref([
    { user_id: 1, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '前端开发工程师', is_followed: true },
    { user_id: 2, username: 'DBA老张', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '数据库管理员', is_followed: true },
    { user_id: 3, username: '运维小李', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'DevOps 工程师', is_followed: false },
    { user_id: 4, username: 'AI大牛', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: '人工智能研究员', is_followed: true }
])
const goBack = () => router.back()
const toggleFollow = (user) => { user.is_followed = !user.is_followed }
</script>

<style scoped>
.follow-list-page { background: #f5f5f5; min-height: 100vh; }
.user-list { padding: 12px; }
.user-item { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.user-info { flex: 1; display: flex; flex-direction: column; }
.user-name { font-size: 15px; color: #333; font-weight: 500; }
.user-bio { font-size: 13px; color: #999; }
</style>
