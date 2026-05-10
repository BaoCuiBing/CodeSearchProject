<template>
    <div class="system-notice-page">
        <PageNavBar title="系统通知" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <div v-else class="notice-list">
            <van-empty v-if="notices.length === 0" description="暂无通知" />
            <div v-for="(notice, index) in notices" :key="notice.notice_id" class="notice-item">
                <div class="notice-time">{{ notice.created_at }}</div>
                <van-collapse v-model="activeNames">
                    <van-collapse-item :title="notice.title" :name="notice.notice_id">
                        <p>{{ notice.content }}</p>
                    </van-collapse-item>
                </van-collapse>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { messageApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const loading = ref(true)
const error = ref('')
const notices = ref([])
const activeNames = ref([])
const loadNotices = async () => {
    loading.value = true
    error.value = ''
    try {
        const data = await messageApi.getNotifications({ type: 'system' })
        notices.value = data?.list || []
        if (notices.value.length > 0) { activeNames.value = [notices.value[0].notice_id] }
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
onMounted(() => { loadNotices(); messageApi.markAllNotificationsRead() })
</script>

<style scoped>
.system-notice-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.notice-list { padding: 12px; }
.notice-item { margin-bottom: 16px; }
.notice-time { text-align: center; font-size: 12px; color: #999; margin-bottom: 8px; }
.notice-item p { margin: 0; font-size: 14px; color: #666; line-height: 1.6; }
</style>