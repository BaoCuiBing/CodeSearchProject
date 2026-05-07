<template>
    <div class="system-notice-page">
        <PageNavBar title="系统通知" />
        <div class="notice-list">
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
const notices = ref([])
const loadNotices = async () => {
    const data = await messageApi.getNotifications({ type: 'system' })
    notices.value = data?.list || []
}
onMounted(() => { loadNotices() })
</script>

<style scoped>
.system-notice-page { background: #f5f5f5; min-height: 100vh; }
.notice-list { padding: 12px; }
.notice-item { margin-bottom: 16px; }
.notice-time { text-align: center; font-size: 12px; color: #999; margin-bottom: 8px; }
.notice-card { background: #fff; border-radius: 8px; padding: 16px; }
.notice-card h4 { margin: 0 0 8px; font-size: 16px; color: #333; }
.notice-card p { margin: 0; font-size: 14px; color: #666; line-height: 1.6; }
</style>
