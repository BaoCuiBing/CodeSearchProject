<template>
    <div class="post-card" @click="$emit('click')">
        <slot name="header" />
        <h4 class="post-title">{{ title }}</h4>
        <p class="post-summary">{{ summary }}</p>
        <slot name="tags" />
        <slot name="footer" />
    </div>
</template>

<script setup>
defineProps({
    title: { type: String, required: true },
    summary: { type: String, default: '' }
})
defineEmits(['click'])
</script>

<style scoped>
.post-card { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.post-title { margin: 0 0 8px; font-size: 16px; color: #333; }
.post-summary { margin: 0; font-size: 14px; color: #666; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>
