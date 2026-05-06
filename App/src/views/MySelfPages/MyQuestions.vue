<template>
    <div class="my-questions-page">
        <PageNavBar title="我的提问" />
        <div class="question-list">
            <PostCard v-for="q in questions" :key="q.question_id" :title="q.title" :summary="q.summary" @click="goToDetail(q.question_id)">
                <template #footer>
                    <div class="question-stats">
                        <span><van-icon name="eye-o" /> {{ q.view_count }}</span>
                        <span><van-icon name="chat-o" /> {{ q.answer_count }}</span>
                    </div>
                </template>
            </PostCard>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageNavBar from '@/components/PageNavBar.vue'
import PostCard from '@/components/PostCard.vue'
const router = useRouter()
const questions = ref([
    { question_id: 1, title: 'Python中如何实现多线程？', summary: '请问Python中如何实现多线程并发？', view_count: 325, answer_count: 12 },
    { question_id: 2, title: 'Vue3响应式原理是什么？', summary: '想了解Vue3的响应式原理', view_count: 218, answer_count: 8 }
])
const goToDetail = (questionId) => { router.push({ path: '/question', query: { id: questionId } }) }
</script>

<style scoped>
.my-questions-page { background: #f5f5f5; min-height: 100vh; }
.question-list { padding: 12px; }
.question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; margin-top: 12px; }
</style>
