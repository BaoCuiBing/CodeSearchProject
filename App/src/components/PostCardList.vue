<template>
    <div class="post-card-list">
        <PostCard v-for="post in posts" :key="post.post_id" :title="post.title" :summary="post.summary" @click="$emit('click', post)">
            <template #header>
                <slot name="header" :post="post" />
            </template>
            <template #tags>
                <slot name="tags" :post="post" />
            </template>
            <template #footer>
                <slot name="footer" :post="post" />
            </template>
        </PostCard>
        <div ref="loadMoreRef" class="load-more-trigger"></div>
        <div v-if="loading" class="loading-text">加载中...</div>
        <div v-else-if="finished" class="finished-text">没有更多了</div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import PostCard from './PostCard.vue'
const props = defineProps({
    loading: { type: Boolean, default: false },
    finished: { type: Boolean, default: false },
    posts: { type: Array, default: () => [] }
})
const emit = defineEmits(['load', 'click'])
const loadMoreRef = ref(null)
let observer = null
const checkAndLoad = () => {
    if (props.loading || props.finished) return
    if (!loadMoreRef.value) return
    const rect = loadMoreRef.value.getBoundingClientRect()
    if (rect.top <= window.innerHeight + 100) {
        emit('load')
    }
}
const initObserver = () => {
    if (observer) { observer.disconnect() }
    if (!loadMoreRef.value || props.finished) return
    observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting && !props.loading && !props.finished) {
                emit('load')
            }
        })
    }, { rootMargin: '200px' })
    observer.observe(loadMoreRef.value)
}
watch(() => props.posts.length, () => {
    nextTick(() => { checkAndLoad() })
})
watch(() => props.loading, (val) => {
    if (!val) {
        nextTick(() => { checkAndLoad() })
    }
})
onMounted(() => {
    nextTick(() => {
        initObserver()
        checkAndLoad()
    })
})
onUnmounted(() => {
    if (observer) { observer.disconnect() }
})
</script>

<style scoped>
.post-card-list {
    padding-bottom: 12px;
}
.load-more-trigger {
    height: 1px;
}
.loading-text,
.finished-text {
    text-align: center;
    padding: 12px 0;
    font-size: 14px;
    color: #999;
}
</style>
