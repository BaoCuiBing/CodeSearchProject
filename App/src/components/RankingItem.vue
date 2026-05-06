<template>
    <div class="ranking-item" @click="$emit('click')">
        <span class="rank-num" :class="{ top: index < 3 }">{{ index + 1 }}</span>
        <slot name="avatar" />
        <div class="rank-content">
            <h4>{{ title }}</h4>
            <p>{{ subtitle }}</p>
        </div>
        <slot name="extra" />
    </div>
</template>

<script setup>
defineProps({
    index: { type: Number, required: true },
    title: { type: String, required: true },
    subtitle: { type: String, default: '' }
})
defineEmits(['click'])
</script>

<style scoped>
.ranking-item { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
.rank-num { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: #999; flex-shrink: 0; }
.rank-num.top { color: #ff6b6b; }
.rank-content { flex: 1; }
.rank-content h4 { margin: 0 0 4px; font-size: 15px; color: #333; }
.rank-content p { margin: 0; font-size: 13px; color: #999; }
</style>
