<template>
    <div class="user-profile-page">
        <PageNavBar v-if="isViewMode" title="用户资料" />
        <PageNavBar v-else title="个人资料" right-text="保存" @click-right="saveProfile" />
        <div v-if="loading" class="loading-wrap">
            <van-loading size="24px" vertical>加载中...</van-loading>
        </div>
        <van-empty v-else-if="error" :description="error" />
        <template v-else>
            <div class="avatar-section">
                <van-image round width="80px" height="80px" :src="profile.avatar || ''" />
                <template v-if="isViewMode">
                    <van-button v-if="profile.is_followed" type="default" size="small" class="follow-btn" @click="toggleFollow">已关注</van-button>
                    <van-button v-else type="primary" size="small" class="follow-btn" @click="toggleFollow">关注</van-button>
                </template>
                <template v-else>
                    <span class="change-avatar" @click="changeAvatar">更换头像</span>
                    <input ref="fileInputRef" type="file" accept="image/*" style="display:none" @change="onFileChange" />
                </template>
            </div>
            <van-cell-group>
                <van-field v-model="profile.username" label="用户名" :readonly="isViewMode" placeholder="请输入用户名" />
                <van-field v-model="profile.bio" label="个人简介" :readonly="isViewMode" placeholder="请输入个人简介" type="textarea" rows="3" />
                <van-field v-model="profile.email" label="邮箱" :readonly="isViewMode" placeholder="请输入邮箱" />
                <van-field v-model="profile.location" label="所在地" :readonly="isViewMode" placeholder="请输入所在地" />
                <van-field v-model="profile.website" label="个人网站" :readonly="isViewMode" placeholder="请输入个人网站" />
                <van-field v-model="profile.github" label="GitHub" :readonly="isViewMode" placeholder="请输入GitHub地址" />
            </van-cell-group>
        </template>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { showToast, showLoadingToast, closeToast } from 'vant'
import { profileApi, uploadApi, followApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
const route = useRoute()
const loading = ref(true)
const error = ref('')
const profile = ref({ username: '', avatar: '', bio: '', email: '', location: '', website: '', github: '', is_followed: false })
const fileInputRef = ref(null)
const viewUserId = computed(() => route.query.id)
const isViewMode = computed(() => viewUserId.value && String(viewUserId.value) !== String(getUserId()))
const loadProfile = async () => {
    loading.value = true
    error.value = ''
    try {
        const userId = isViewMode.value ? viewUserId.value : getUserId()
        const data = await profileApi.getProfile(userId)
        profile.value = data || {}
    } catch (err) {
        error.value = err.message || '加载失败'
    } finally {
        loading.value = false
    }
}
const saveProfile = async () => {
    await profileApi.updateProfile(profile.value)
    showToast('保存成功')
}
const changeAvatar = () => { fileInputRef.value.click() }
const onFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    showLoadingToast({ message: '上传中...', forbidClick: true })
    try {
        const data = await uploadApi.uploadFile(file)
        profile.value.avatar = data.file_url
        await profileApi.updateProfile({ avatar: data.file_url })
        closeToast()
        showToast('头像更换成功')
    } catch (err) {
        closeToast()
    }
}
const toggleFollow = async () => {
    try {
        const data = await followApi.toggleFollow(viewUserId.value)
        profile.value.is_followed = data.is_followed
        showToast(data.is_followed ? '已关注' : '已取消关注')
    } catch (err) {
        showToast(err.message || '操作失败')
    }
}
onMounted(() => { loadProfile() })
</script>

<style scoped>
.user-profile-page { background: #f5f5f5; min-height: 100vh; }
.loading-wrap { display: flex; justify-content: center; align-items: center; padding: 80px 0; }
.error-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; gap: 12px; }
.error-text { font-size: 14px; color: #999; }
.avatar-section { display: flex; flex-direction: column; align-items: center; padding: 24px; background: #fff; margin-bottom: 8px; }
.change-avatar { margin-top: 12px; color: #1989fa; font-size: 14px; }
.follow-btn { margin-top: 12px; }
</style>