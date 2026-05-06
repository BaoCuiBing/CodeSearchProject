<template>
    <div class="my-questions-page">
        <van-nav-bar title="我的提问" left-arrow @click-left="goBack" fixed placeholder />
        <div class="question-list">
            <div v-for="q in questions" :key="q.question_id" class="question-card" @click="goToDetail(q.question_id)">
                <h4>{{ q.title }}</h4>
                <p>{{ q.summary }}</p>
                <div class="question-stats">
                    <span><van-icon name="eye-o" /> {{ q.view_count }}</span>
                    <span><van-icon name="chat-o" /> {{ q.answer_count }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const questions = ref([
    { question_id: 1, title: 'Python中如何实现多线程？', summary: '请问Python中如何实现多线程并发？', view_count: 325, answer_count: 12 },
    { question_id: 2, title: 'Vue3响应式原理是什么？', summary: '想了解Vue3的响应式原理', view_count: 218, answer_count: 8 }
])
const goBack = () => router.back()
const goToDetail = (questionId) => { router.push({ path: '/question', query: { id: questionId } }) }
</script>

<style scoped>
.my-questions-page { background: #f5f5f5; min-height: 100vh; }
.question-list { padding: 12px; }
.question-card { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.question-card h4 { margin: 0 0 8px; font-size: 16px; }
.question-card p { margin: 0 0 12px; font-size: 14px; color: #666; }
.question-stats { display: flex; gap: 16px; font-size: 13px; color: #999; }
</style>
