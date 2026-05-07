<template>
    <div class="user-list-item">
        <van-image round width="48px" height="48px" :src="avatar" />
        <div class="user-info">
            <span class="user-name">{{ username }}</span>
            <span class="user-bio">{{ bio || '这个人很懒，什么都没写' }}</span>
        </div>
        <van-button size="small" :type="isFollowed ? 'default' : 'primary'" :plain="plain" @click.stop="$emit('toggle')">{{ isFollowed ? followedText : followText }}</van-button>
    </div>
</template>

<script setup>
defineProps({
    avatar: { type: String, required: true },
    username: { type: String, required: true },
    bio: { type: String, default: '' },
    isFollowed: { type: Boolean, default: false },
    followText: { type: String, default: '关注' },
    followedText: { type: String, default: '已关注' },
    plain: { type: Boolean, default: false }
})
defineEmits(['toggle'])
</script>

<style scoped>
.user-list-item { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
.user-info { flex: 1; display: flex; flex-direction: column; }
.user-name { font-size: 15px; color: #333; font-weight: 500; }
.user-bio { font-size: 13px; color: #999; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; }
</style>
