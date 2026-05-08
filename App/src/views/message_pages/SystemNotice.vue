<template>
    <div class="system-notice-page">
        <PageNavBar title="系统通知" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <div v-else-if="error" class="error-wrap">
            <van-icon name="warn-o" size="48" color="#999" />
            <p class="error-text">{{ error }}</p>
            <van-button type="primary" size="small" @click="loadNotices">重试</van-button>
        </div>
        <div v-else class="notice-list">
            <van-empty v-if="notices.length === 0" description="暂无通知" />
            <div v-for="notice in notices" :key="notice.notice_id" class="notice-item">
                <div class="notice-time">{{ notice.created_at }}</div>
                <div class="notice-card">
                    <h4>{{ notice.title }}</h4>
                    <p>{{ notice.content }}</p>
                </div>
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
const loadNotices = async () => {
    loading.value = true
    error.value = ''
    try {
        const data = await messageApi.getNotifications({ type: 'system' })
        notices.value = data?.list || []
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
onMounted(() => { loadNotices() })
</script>

<style scoped>
.system-notice-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.notice-list { padding: 12px; }
.notice-item { margin-bottom: 16px; }
.notice-time { text-align: center; font-size: 12px; color: #999; margin-bottom: 8px; }
.notice-card { background: #fff; border-radius: 8px; padding: 16px; }
.notice-card h4 { margin: 0 0 8px; font-size: 16px; color: #333; }
.notice-card p { margin: 0; font-size: 14px; color: #666; line-height: 1.6; }
</style>