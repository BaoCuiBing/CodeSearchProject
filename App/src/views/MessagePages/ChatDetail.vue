<template>
    <div class="chat-detail-page">
        <van-nav-bar :title="chatUser.username" left-arrow @click-left="goBack" fixed placeholder />
        <div class="chat-messages">
            <div v-for="msg in messages" :key="msg.id" class="chat-bubble" :class="{ self: msg.from_user_id === selfUserId }">
                <van-image round width="36px" height="36px" :src="msg.from_user_id === selfUserId ? selfAvatar : chatUser.avatar" />
                <div class="bubble-content">{{ msg.content }}</div>
            </div>
        </div>
        <div class="chat-input">
            <van-field v-model="inputMessage" placeholder="输入消息..." />
            <van-button type="primary" size="small" @click="sendMessage">发送</van-button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const chatUser = ref({ user_id: route.query.user_id || 1, username: route.query.username || '用户A', avatar: route.query.avatar || 'https://img.yzcdn.cn/vant/cat.jpeg' })
const selfAvatar = ref('https://img.yzcdn.cn/vant/cat.jpeg')
const selfUserId = ref(1)
const inputMessage = ref('')
const messages = ref([
    { id: 1, from_user_id: 10, to_user_id: 1, content: '你好，请问那个 Python 多线程的问题解决了吗？', is_read: 1, created_at: '2025-05-05 14:30:00' },
    { id: 2, from_user_id: 1, to_user_id: 10, content: '还没完全解决，正在研究中', is_read: 1, created_at: '2025-05-05 14:32:00' },
    { id: 3, from_user_id: 10, to_user_id: 1, content: '需要我帮忙看看吗？', is_read: 1, created_at: '2025-05-05 14:35:00' },
    { id: 4, from_user_id: 1, to_user_id: 10, content: '太好了，谢谢！', is_read: 1, created_at: '2025-05-05 14:36:00' }
])
const goBack = () => router.back()
const sendMessage = () => {
    if (inputMessage.value.trim()) {
        messages.value.push({ id: Date.now(), from_user_id: selfUserId.value, to_user_id: chatUser.value.user_id, content: inputMessage.value, is_read: 0, created_at: new Date().toLocaleString() })
        inputMessage.value = ''
    }
}
</script>

<style scoped>
.chat-detail-page { background: #f5f5f5; min-height: 100vh; display: flex; flex-direction: column; }
.chat-messages { flex: 1; padding: 16px; overflow-y: auto; }
.chat-bubble { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 16px; }
.chat-bubble.self { flex-direction: row-reverse; }
.bubble-content { max-width: 70%; padding: 12px 16px; border-radius: 16px; background: #fff; font-size: 14px; color: #333; line-height: 1.5; }
.chat-bubble.self .bubble-content { background: #1989fa; color: #fff; }
.chat-input { display: flex; align-items: center; gap: 8px; padding: 12px; background: #fff; border-top: 1px solid #eee; }
.chat-input .van-field { flex: 1; }
</style>
