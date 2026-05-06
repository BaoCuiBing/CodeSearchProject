<template>
    <div class="followers-page">
        <van-nav-bar title="我的粉丝" left-arrow @click-left="goBack" fixed placeholder />
        <div class="user-list">
            <div v-for="user in followersList" :key="user.user_id" class="user-item">
                <van-image round width="48px" height="48px" :src="user.avatar" />
                <div class="user-info">
                    <h4>{{ user.username }}</h4>
                    <p>{{ user.bio || '这个人很懒，什么都没写' }}</p>
                </div>
                <van-button size="small" :type="user.is_followed ? 'default' : 'primary'" @click="followBack(user.user_id)">{{ user.is_followed ? '已关注' : '回关' }}</van-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
const router = useRouter()
const followersList = ref([
    { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'Python开发者', is_followed: false },
    { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'Vue3爱好者', is_followed: false }
])
const goBack = () => router.back()
const followBack = (userId) => { const user = followersList.value.find(u => u.user_id === userId); if (user) { user.is_followed = true; showToast('已关注') } }
</script>

<style scoped>
.followers-page { background: #f5f5f5; min-height: 100vh; }
.user-list { padding: 12px; }
.user-item { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
.user-info { flex: 1; }
.user-info h4 { margin: 0 0 4px; font-size: 15px; color: #333; }
.user-info p { margin: 0; font-size: 13px; color: #999; }
</style>
