<template>
    <div class="system-notice-page">
        <van-nav-bar title="系统通知" left-arrow @click-left="goBack" fixed placeholder />
        <div class="notice-list">
            <div v-for="notice in notices" :key="notice.id" class="notice-item">
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const notices = ref([
    { id: 1, title: '系统维护通知', content: '系统将于今晚 00:00-02:00 进行维护升级，期间部分功能可能无法使用，请提前做好准备。', created_at: '2025-05-05' },
    { id: 2, title: '新功能上线', content: '文章收藏功能已上线，现在你可以收藏喜欢的文章以便后续查看。', created_at: '2025-05-03' },
    { id: 3, title: '社区规范更新', content: '社区内容规范已更新，请前往查看并遵守相关规定。', created_at: '2025-05-01' }
])
const goBack = () => router.back()
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
