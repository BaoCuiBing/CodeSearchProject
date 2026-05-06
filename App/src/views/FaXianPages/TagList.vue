<template>
    <div class="tag-list-page">
        <van-nav-bar title="标签" left-arrow @click-left="goBack" fixed placeholder />
        <div class="tag-section">
            <div class="section-title">热门标签</div>
            <div class="tag-cloud">
                <van-tag v-for="tag in hotTags" :key="tag.tag_id" :color="tag.color" size="large" class="cloud-tag" @click="goToTag(tag.tag_id)">{{ tag.name }}</van-tag>
            </div>
        </div>
        <div class="tag-section">
            <div class="section-title">全部标签</div>
            <div class="tag-list">
                <div v-for="tag in allTags" :key="tag.tag_id" class="tag-item" @click="goToTag(tag.tag_id)">
                    <van-tag :color="tag.color" plain>{{ tag.name }}</van-tag>
                    <span class="tag-count">{{ tag.post_count }} 篇文章</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const hotTags = ref([
    { tag_id: 1, name: 'Python', color: '#1989fa' },
    { tag_id: 2, name: 'JavaScript', color: '#ff6b6b' },
    { tag_id: 3, name: 'Vue', color: '#42b883' },
    { tag_id: 4, name: 'React', color: '#61dafb' },
    { tag_id: 5, name: 'Docker', color: '#2496ed' },
    { tag_id: 6, name: 'MySQL', color: '#4479a1' },
    { tag_id: 7, name: 'Redis', color: '#dc382d' },
    { tag_id: 8, name: 'Linux', color: '#fcc624' }
])
const allTags = ref([
    { tag_id: 1, name: 'Python', color: '#1989fa', post_count: 156 },
    { tag_id: 2, name: 'JavaScript', color: '#ff6b6b', post_count: 134 },
    { tag_id: 3, name: 'Vue', color: '#42b883', post_count: 89 },
    { tag_id: 4, name: 'React', color: '#61dafb', post_count: 76 },
    { tag_id: 5, name: 'Docker', color: '#2496ed', post_count: 65 },
    { tag_id: 6, name: 'MySQL', color: '#4479a1', post_count: 98 },
    { tag_id: 7, name: 'Redis', color: '#dc382d', post_count: 45 },
    { tag_id: 8, name: 'Linux', color: '#fcc624', post_count: 72 },
    { tag_id: 9, name: 'Go', color: '#00add8', post_count: 54 },
    { tag_id: 10, name: 'Java', color: '#007396', post_count: 112 }
])
const goBack = () => router.back()
const goToTag = (tagId) => { router.push({ path: '/tag', query: { id: tagId } }) }
</script>

<style scoped>
.tag-list-page { background: #f5f5f5; min-height: 100vh; }
.tag-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.section-title { font-size: 16px; font-weight: 500; margin-bottom: 16px; }
.tag-cloud { display: flex; flex-wrap: wrap; gap: 12px; }
.cloud-tag { padding: 8px 16px; }
.tag-list { display: flex; flex-direction: column; gap: 12px; }
.tag-item { display: flex; align-items: center; justify-content: space-between; padding: 12px; background: #f9f9f9; border-radius: 8px; }
.tag-count { font-size: 13px; color: #999; }
</style>
