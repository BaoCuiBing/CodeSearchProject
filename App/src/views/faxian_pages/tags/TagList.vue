<template>
    <div class="tag-list-page">
        <PageNavBar title="标签" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <template v-else>
            <div class="tag-section">
                <div class="section-title">热门标签</div>
                <div class="tag-cloud">
                    <van-empty v-if="hotTags.length === 0" description="暂无热门标签" />
                    <van-tag v-for="tag in hotTags" :key="tag.tag_id" :color="tag.color" size="large" class="cloud-tag" @click="goToTag(tag.tag_id, tag.name)">{{ tag.name }}</van-tag>
                </div>
            </div>
            <div class="tag-section">
                <div class="section-title">全部标签</div>
                <div class="tag-list">
                    <van-empty v-if="allTags.length === 0" description="暂无标签" />
                    <div v-for="tag in allTags" :key="tag.tag_id" class="tag-item" @click="goToTag(tag.tag_id, tag.name)">
                        <van-tag :color="tag.color" plain>{{ tag.name }}</van-tag>
                        <span class="tag-count">{{ tag.post_count }} 篇文章</span>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { tagApi } from '@/assets/app_request_api.js'
import PageNavBar from '@/components/PageNavBar.vue'
const router = useRouter()
const loading = ref(true)
const error = ref('')
const hotTags = ref([])
const allTags = ref([])
const loadHotTags = async () => {
    const data = await tagApi.getHotTags(8)
    hotTags.value = data || []
}
const loadAllTags = async () => {
    const data = await tagApi.getList({ page: 1, page_size: 100 })
    allTags.value = data?.list || []
}
const loadAll = async () => {
    loading.value = true
    error.value = ''
    try {
        await Promise.all([loadHotTags(), loadAllTags()])
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const goToTag = (tagId, tagName) => { router.push({ path: '/tag', query: { id: tagId, name: tagName } }) }
onMounted(() => { loadAll() })
</script>

<style scoped>
.tag-list-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.tag-section { background: #fff; padding: 16px; margin-bottom: 8px; }
.section-title { font-size: 16px; font-weight: 500; margin-bottom: 16px; }
.tag-cloud { display: flex; flex-wrap: wrap; gap: 12px; }
.cloud-tag { padding: 8px 16px; cursor: pointer; }
.tag-list { display: flex; flex-direction: column; gap: 12px; }
.tag-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; cursor: pointer; }
.tag-count { font-size: 14px; color: #999; }
</style>