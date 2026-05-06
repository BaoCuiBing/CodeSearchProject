<template>
    <div class="following-page">
        <van-nav-bar title="我的关注" left-arrow @click-left="goBack" fixed placeholder />
        <div class="user-list">
            <div v-for="user in followingList" :key="user.user_id" class="user-item">
                <van-image round width="48px" height="48px" :src="user.avatar" />
                <div class="user-info">
                    <h4>{{ user.username }}</h4>
                    <p>{{ user.bio || '这个人很懒，什么都没写' }}</p>
                </div>
                <van-button size="small" :type="user.is_followed ? 'default' : 'primary'" plain @click="unfollow(user.user_id)">{{ user.is_followed ? '已关注' : '关注' }}</van-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
const router = useRouter()
const followingList = ref([
    { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'Python开发者', is_followed: true },
    { user_id: 2, username: '前端小王', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', bio: 'Vue3爱好者', is_followed: true }
])
const goBack = () => router.back()
const unfollow = (userId) => { const user = followingList.value.find(u => u.user_id === userId); if (user) { user.is_followed = false; showToast('已取消关注') } }
</script>

<style scoped>
.following-page { background: #f5f5f5; min-height: 100vh; }
.user-list { padding: 12px; }
.user-item { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
.user-info { flex: 1; }
.user-info h4 { margin: 0 0 4px; font-size: 15px; color: #333; }
.user-info p { margin: 0; font-size: 13px; color: #999; }
</style>
