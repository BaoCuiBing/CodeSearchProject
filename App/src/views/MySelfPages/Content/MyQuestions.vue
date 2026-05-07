<template>
    <div class="my-questions-page">
        <PageNavBar title="我的提问" />
        <div class="question-list">
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
const questions = ref([])
const loadQuestions = async () => {
    const data = await articleApi.getList({ user_id: getUserId(), type: 'question', page: 1 })
    questions.value = data?.list || []
}
const goToDetail = (questionId) => { router.push({ path: '/article', query: { id: questionId } }) }
onMounted(() => { loadQuestions() })
</script>

<style scoped>
.my-questions-page { background: #f5f5f5; min-height: 100vh; }
.question-list { padding: 12px; }
.question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
