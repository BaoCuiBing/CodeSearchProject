<template>
    <div class="my-questions-page">
        <PageNavBar title="我的提问" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <div v-else class="question-list">
            <van-empty v-if="questions.length === 0" description="暂无提问" />
            <PostCard v-for="q in questions" :key="q.post_id" :title="q.title" :summary="q.summary" @click="goToDetail(q.post_id)">
                <template #footer>
                    <div class="question-stats">
                        <span><van-icon name="eye-o" /> {{ q.view_count }}</span>
                        <span><van-icon name="chat-o" /> {{ q.comment_count }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const loading = ref(true)
const error = ref('')
const questions = ref([])
const loadQuestions = async () => {
    loading.value = true
    error.value = ''
    try {
        const data = await articleApi.getList({ user_id: getUserId(), type: 'question', page: 1 })
        questions.value = data?.list || []
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const goToDetail = (questionId) => { router.push({ path: '/article', query: { id: questionId } }) }
onMounted(() => { loadQuestions() })
</script>

<style scoped>
.my-questions-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.question-list { padding: 12px; }
.question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>