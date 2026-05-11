<template>
    <div class="message-page">
        <van-nav-bar title="消息" fixed placeholder />
        <div class="message-header">
            <h2>消息</h2>
            <span class="read-all" @click="markAllRead">全部已读</span>
        </div>
        <div class="message-tabs">
            <van-tabs v-model:active="activeTab" @change="onTabChange">
                <van-tab title="全部">
                    <div v-if="notificationsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                    <van-empty v-else-if="notificationsError" :description="notificationsError" />
                    <div v-else class="message-list">
                        <van-empty v-if="allMessages.length === 0" description="暂无消息" />
                        <van-swipe-cell v-for="msg in allMessages" :key="msg.notification_id">
                            <div class="message-item" :class="{ unread: !msg.is_read }" @click="msg.type === 'chat' ? goToChat(msg) : goToDetail(msg)">
                                <template v-if="msg.type === 'chat'">
                                    <van-image round width="40px" height="40px" :src="msg.actor?.avatar || ''" />
                                    <div class="msg-content">
                                        <div class="msg-title">{{ msg.actor?.username || '' }}：{{ msg.content }}</div>
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
                            <template #right>
                                <van-button square type="danger" text="删除" @click="handleDeleteNotification(msg)" />
                            </template>
                        </van-swipe-cell>
                    </div>
                </van-tab>
                <van-tab title="私信">
                    <div v-if="chatsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                    <van-empty v-else-if="chatsError" :description="chatsError" />
                    <div v-else class="message-list">
                        <van-empty v-if="privateChats.length === 0" description="暂无私信" />
                        <van-swipe-cell v-for="chat in privateChats" :key="chat.user?.user_id">
                            <div class="message-item" :class="{ unread: chat.unread_count > 0 }" @click="goToChat(chat)">
                                <van-image round width="40px" height="40px" :src="chat.user?.avatar" />
                                <div class="msg-content">
                                    <div class="msg-title">{{ chat.user?.username }}</div>
                                    <div class="msg-time">{{ chat.last_message }}</div>
                                </div>
                                <van-badge v-if="chat.unread_count > 0" :content="chat.unread_count" color="#ff6b6b" />
                            </div>
                            <template #right>
                                <van-button square type="danger" text="删除" @click="deleteConversation(chat)" />
                            </template>
                        </van-swipe-cell>
                    </div>
                </van-tab>
                <van-tab title="评论">
                    <div v-if="notificationsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                    <van-empty v-else-if="notificationsError" :description="notificationsError" />
                    <div v-else class="message-list">
                        <van-empty v-if="commentMessages.length === 0" description="暂无评论" />
                        <van-swipe-cell v-for="msg in commentMessages" :key="msg.notification_id">
                            <div class="message-item" :class="{ unread: !msg.is_read }" @click="goToDetail(msg)">
                                <van-image round width="40px" height="40px" :src="msg.actor?.avatar || ''" />
                                <div class="msg-content">
                                    <div class="msg-title">{{ msg.actor?.username || '' }} {{ msg.content }}</div>
                                    <div class="msg-time">{{ msg.created_at }}</div>
                                </div>
                                <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                            </div>
                            <template #right>
                                <van-button square type="danger" text="删除" @click="handleDeleteNotification(msg)" />
                            </template>
                        </van-swipe-cell>
                    </div>
                </van-tab>
                <van-tab title="点赞">
                    <div v-if="notificationsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                    <van-empty v-else-if="notificationsError" :description="notificationsError" />
                    <div v-else class="message-list">
                        <van-empty v-if="likeMessages.length === 0" description="暂无点赞" />
                        <van-swipe-cell v-for="msg in likeMessages" :key="msg.notification_id">
                            <div class="message-item" :class="{ unread: !msg.is_read }" @click="goToDetail(msg)">
                                <van-image round width="40px" height="40px" :src="msg.actor?.avatar || ''" />
                                <div class="msg-content">
                                    <div class="msg-title">{{ msg.actor?.username || '' }} {{ msg.content }}</div>
                                    <div class="msg-time">{{ msg.created_at }}</div>
                                </div>
                                <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                            </div>
                            <template #right>
                                <van-button square type="danger" text="删除" @click="handleDeleteNotification(msg)" />
                            </template>
                        </van-swipe-cell>
                    </div>
                </van-tab>
                <van-tab title="关注">
                    <div v-if="notificationsLoading" class="section-loading"><van-loading size="20px" vertical>加载中...</van-loading></div>
                    <van-empty v-else-if="notificationsError" :description="notificationsError" />
                    <div v-else class="message-list">
                        <van-empty v-if="followMessages.length === 0" description="暂无关注" />
                        <van-swipe-cell v-for="msg in followMessages" :key="msg.notification_id">
                            <div class="message-item" :class="{ unread: !msg.is_read }" @click="goToDetail(msg)">
                                <van-image round width="40px" height="40px" :src="msg.actor?.avatar || ''" />
                                <div class="msg-content">
                                    <div class="msg-title">{{ msg.actor?.username || '' }} {{ msg.content }}</div>
                                    <div class="msg-time">{{ msg.created_at }}</div>
                                </div>
                                <van-badge v-if="!msg.is_read" dot color="#ff6b6b" />
                            </div>
                            <template #right>
                                <van-button square type="danger" text="删除" @click="handleDeleteNotification(msg)" />
                            </template>
                        </van-swipe-cell>
                    </div>
                </van-tab>
            </van-tabs>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import { messageApi } from '@/assets/app_request_api.js'
const router = useRouter()
const activeTab = ref(0)
const notificationsLoading = ref(true)
const notificationsError = ref('')
const chatsLoading = ref(true)
const chatsError = ref('')
const allMessages = ref([])
const privateChats = ref([])
const commentMessages = computed(() => allMessages.value.filter(m => m.type === 'comment'))
const likeMessages = computed(() => allMessages.value.filter(m => m.type === 'like'))
const followMessages = computed(() => allMessages.value.filter(m => m.type === 'follow'))
const loadNotifications = async () => {
    notificationsLoading.value = true
    notificationsError.value = ''
    try {
        const data = await messageApi.getNotifications({ type: 'all' })
        allMessages.value = data?.list || []
    } catch (err) {
        notificationsError.value = err.message || '加载失败'
    } finally {
        notificationsLoading.value = false
    }
}
const loadConversations = async () => {
    chatsLoading.value = true
    chatsError.value = ''
    try {
        const data = await messageApi.getConversations(1, 20)
        privateChats.value = data?.list || []
    } catch (err) {
        chatsError.value = err.message || '加载失败'
    } finally {
        chatsLoading.value = false
    }
}
const loadAll = async () => {
    await Promise.all([loadNotifications(), loadConversations()])
}
const onTabChange = async (index) => {
    if (index === 0) { await loadNotifications() }
    if (index === 1) { await loadConversations() }
    if (index === 2) { const data = await messageApi.getNotifications({ type: 'comment' }); allMessages.value = data?.list || [] }
    if (index === 3) { const data = await messageApi.getNotifications({ type: 'like' }); allMessages.value = data?.list || [] }
    if (index === 4) { const data = await messageApi.getNotifications({ type: 'follow' }); allMessages.value = data?.list || [] }
}
const markAllRead = async () => {
    await messageApi.markAllNotificationsRead()
    allMessages.value.forEach(m => m.is_read = true)
    loadUnreadCount()
}
const loadUnreadCount = async () => {
    try {
        const data = await messageApi.getUnreadCount()
        const event = new CustomEvent('update-unread-count', { detail: data?.total || 0 })
        window.dispatchEvent(event)
    } catch (e) { /* 忽略 */ }
}
const getIcon = (type) => {
    const icons = { comment: 'comment-o', like: 'good-job-o', follow: 'user-o', system: 'bullhorn-o' }
    return icons[type] || 'bell-o'
}
const goToDetail = async (msg) => {
    if (!msg.is_read) {
        msg.is_read = true
        await messageApi.markNotificationRead(msg.notification_id)
        loadUnreadCount()
    }
    if (msg.type === 'system') { router.push('/system-notice') }
    else if (msg.type === 'follow') { router.push({ path: '/profile', query: { id: msg.related_id } }) }
    else if (msg.related_id > 0) {
        const query = { id: msg.related_id }
        if (msg.type === 'comment') { query.highlight_comment = 'all' }
        else if (msg.type === 'like') { query.highlight_comment = 'input' }
        router.push({ path: '/article', query })
    }
}
const goToChat = async (chat) => {
    const userId = chat.user?.user_id || chat.actor?.user_id
    const username = chat.user?.username || chat.actor?.username
    const avatar = chat.user?.avatar || chat.actor?.avatar
    await messageApi.markConversationRead(userId)
    if (chat.unread_count !== undefined) { chat.unread_count = 0 }
    router.push({ path: '/chat', query: { user_id: userId, username: username, avatar: avatar } })
}
const deleteConversation = async (chat) => {
    await messageApi.deleteConversation(chat.user?.user_id)
    privateChats.value = privateChats.value.filter(c => c.user?.user_id !== chat.user?.user_id)
}
const handleDeleteNotification = async (msg) => {
    try {
        await showConfirmDialog({ title: '确认删除', message: '确定要删除这条消息吗？' })
        await messageApi.deleteNotification(msg.notification_id)
        allMessages.value = allMessages.value.filter(m => m.notification_id !== msg.notification_id)
        loadUnreadCount()
        showToast('已删除')
    } catch (e) { /* 用户取消 */ }
}
onMounted(() => { loadAll() })
</script>

<style scoped>
.message-page { padding-bottom: 60px; background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.section-loading { display: flex; justify-content: center; align-items: center; padding: 40px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
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
.msg-title { font-size: 14px; color: #333; line-height: 1.5; margin-bottom: 4px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.msg-time { font-size: 12px; color: #999; }
.bottom-spacer { height: 80px; }
</style>