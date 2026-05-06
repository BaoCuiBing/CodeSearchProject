<template>
    <div class="message-page">
        <van-nav-bar title="消息" fixed placeholder />
        <div class="message-header">
            <h2>消息</h2>
            <span class="read-all" @click="markAllRead">全部已读</span>
        </div>
        <div class="message-tabs">
            <van-tabs v-model:active="activeTab">
                <van-tab title="全部">
                    <div class="message-list">
                        <div v-for="msg in allMessages" :key="msg.notification_id" class="message-item" :class="{ unread: !msg.is_read }" @click="msg.type === 'chat' ? goToChat(msg) : goToDetail(msg)">
                            <template v-if="msg.type === 'chat'">
                                <van-image round width="40px" height="40px" :src="msg.actor.avatar" />
                                <div class="msg-content">
                                    <div class="msg-title">{{ msg.actor.username }}：{{ msg.content }}</div>
                                    <div class="msg-time">{{ msg.created_at }}</div>
                                </div>
                                <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                            </template>
                            <template v-else>
                                <div class="msg-icon" :class="msg.type">
                                    <van-icon :name="getIcon(msg.type)" color="#fff" size="20" />
                                </div>
                                <div class="msg-content">
                                    <div class="msg-title">{{ msg.content }}</div>
                                    <div class="msg-time">{{ msg.created_at }}</div>
                                </div>
                                <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                            </template>
                        </div>
                    </div>
                </van-tab>
                <van-tab title="私信">
                    <div class="message-list">
                        <div v-for="chat in privateChats" :key="chat.user_id" class="message-item" :class="{ unread: chat.unread_count > 0 }" @click="goToChat(chat)">
                            <van-image round width="40px" height="40px" :src="chat.avatar" />
                            <div class="msg-content">
                                <div class="msg-title">{{ chat.username }}</div>
                                <div class="msg-time">{{ chat.last_message }}</div>
                            </div>
                            <van-badge v-if="chat.unread_count > 0" :content="chat.unread_count" color="#ff6b6b" />
                        </div>
                    </div>
                </van-tab>
                <van-tab title="评论">
                    <div class="message-list">
                        <div v-for="msg in commentMessages" :key="msg.notification_id" class="message-item" :class="{ unread: !msg.is_read }" @click="goToDetail(msg)">
                            <van-image round width="40px" height="40px" :src="msg.actor.avatar" />
                            <div class="msg-content">
                                <div class="msg-title">{{ msg.actor.username }} {{ msg.content }}</div>
                                <div class="msg-time">{{ msg.created_at }}</div>
                            </div>
                            <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                        </div>
                    </div>
                </van-tab>
                <van-tab title="点赞">
                    <div class="message-list">
                        <div v-for="msg in likeMessages" :key="msg.notification_id" class="message-item" :class="{ unread: !msg.is_read }" @click="goToDetail(msg)">
                            <van-image round width="40px" height="40px" :src="msg.actor.avatar" />
                            <div class="msg-content">
                                <div class="msg-title">{{ msg.actor.username }} {{ msg.content }}</div>
                                <div class="msg-time">{{ msg.created_at }}</div>
                            </div>
                            <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                        </div>
                    </div>
                </van-tab>
                <van-tab title="关注">
                    <div class="message-list">
                        <div v-for="msg in followMessages" :key="msg.notification_id" class="message-item" :class="{ unread: !msg.is_read }" @click="goToDetail(msg)">
                            <van-image round width="40px" height="40px" :src="msg.actor.avatar" />
                            <div class="msg-content">
                                <div class="msg-title">{{ msg.actor.username }} {{ msg.content }}</div>
                                <div class="msg-time">{{ msg.created_at }}</div>
                            </div>
                            <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                        </div>
                    </div>
                </van-tab>
            </van-tabs>
        </div>
        <div class="bottom-spacer"></div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const activeTab = ref(0)
const privateChats = ref([
    { user_id: 10, username: '用户A', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', last_message: '你好，请问那个 Python 多线程的问题解决了吗？', unread_count: 2, created_at: '2025-05-05 14:30:00' },
    { user_id: 11, username: '用户B', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', last_message: '需要我帮忙看看吗？', unread_count: 0, created_at: '2025-05-05 13:00:00' },
    { user_id: 12, username: '用户C', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', last_message: '感谢分享！', unread_count: 1, created_at: '2025-05-05 12:00:00' },
    { user_id: 13, username: '用户D', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg', last_message: '后面慢慢看', unread_count: 0, created_at: '2025-05-05 11:00:00' }
])
const allMessages = ref([
    { notification_id: 1, type: 'chat', content: '你好，请问那个 Python 多线程的问题解决了吗？', is_read: false, actor: { user_id: 10, username: '用户A', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, created_at: '2025-05-05 14:30:00', related_id: 10 },
    { notification_id: 2, type: 'comment', content: '评论了你的文章《如何在 Python 中实现多线程并发？》', is_read: false, actor: { user_id: 10, username: '用户A', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, created_at: '2025-05-05 14:30:00', related_id: 1 },
    { notification_id: 3, type: 'like', content: '赞了你的文章', is_read: false, actor: { user_id: 11, username: '用户B', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, created_at: '2025-05-05 13:00:00', related_id: 1 },
    { notification_id: 4, type: 'follow', content: '关注了你', is_read: true, actor: { user_id: 12, username: '用户C', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, created_at: '2025-05-05 12:00:00', related_id: 3 },
    { notification_id: 5, type: 'system', content: '系统通知：你的文章已通过审核', is_read: true, actor: null, created_at: '2025-05-05 11:00:00', related_id: 0 },
    { notification_id: 6, type: 'comment', content: '回复了你的评论', is_read: false, actor: { user_id: 13, username: '用户D', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, created_at: '2025-05-05 10:00:00', related_id: 2 },
    { notification_id: 7, type: 'chat', content: '需要我帮忙看看吗？', is_read: false, actor: { user_id: 11, username: '用户B', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' }, created_at: '2025-05-05 09:30:00', related_id: 11 }
])
const commentMessages = computed(() => allMessages.value.filter(m => m.type === 'comment'))
const likeMessages = computed(() => allMessages.value.filter(m => m.type === 'like'))
const followMessages = computed(() => allMessages.value.filter(m => m.type === 'follow'))
const getIcon = (type) => {
    const icons = { comment: 'comment-o', like: 'good-job-o', follow: 'user-o', system: 'bullhorn-o' }
    return icons[type] || 'bell-o'
}
const markAllRead = () => { allMessages.value.forEach(m => m.is_read = true) }
const goToDetail = (msg) => {
    if (msg.type === 'system') { router.push('/system-notice') }
    else if (msg.type === 'follow') { router.push({ path: '/profile', query: { id: msg.related_id } }) }
    else if (msg.related_id > 0) { router.push({ path: '/article', query: { id: msg.related_id } }) }
}
const goToChat = (chat) => { 
    const userId = chat.user_id || chat.actor?.user_id
    const username = chat.username || chat.actor?.username
    const avatar = chat.avatar || chat.actor?.avatar
    router.push({ path: '/chat', query: { user_id: userId, username: username, avatar: avatar } }) 
}
</script>

<style scoped>
.message-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.message-header { display: flex; justify-content: space-between; align-items: center; padding: 16px; background: #fff; }
.message-header h2 { margin: 0; font-size: 20px; color: #333; }
.read-all { color: #1989fa; font-size: 14px; }
.message-tabs { background: #fff; }
.message-list { padding: 12px; }
.message-item { display: flex; align-items: center; gap: 12px; padding: 16px; background: #fff; border-radius: 8px; margin-bottom: 8px; }
.message-item.unread { background: #f0f8ff; }
.msg-icon { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.msg-icon.comment { background: #1989fa; }
.msg-icon.like { background: #ff6b6b; }
.msg-icon.follow { background: #42b883; }
.msg-icon.system { background: #ff976a; }
.msg-content { flex: 1; }
.msg-title { font-size: 14px; color: #333; line-height: 1.5; margin-bottom: 4px; }
.msg-time { font-size: 12px; color: #999; }
.bottom-spacer { height: 80px; }
</style>
