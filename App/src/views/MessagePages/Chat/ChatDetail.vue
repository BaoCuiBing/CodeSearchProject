<template>
    <div class="chat-detail-page">
        <PageNavBar :title="chatUser.username" />
        <div class="chat-messages">
            <div v-for="msg in messages" :key="msg.message_id" class="chat-bubble" :class="{ self: msg.from_user_id === selfUserId }">
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { messageApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
const route = useRoute()
const chatUser = ref({ user_id: route.query.user_id || 1, username: route.query.username || '用户', avatar: route.query.avatar || '' })
const selfAvatar = ref('')
const selfUserId = ref(getUserId())
const inputMessage = ref('')
const messages = ref([])
const loadMessages = async () => {
    const data = await messageApi.getConversationMessages(chatUser.value.user_id, 1, 20)
    messages.value = data?.list || []
}
const sendMessage = async () => {
    if (!inputMessage.value.trim()) return
    await messageApi.sendMessage(chatUser.value.user_id, inputMessage.value)
    inputMessage.value = ''
    loadMessages()
}
onMounted(() => { loadMessages() })
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
