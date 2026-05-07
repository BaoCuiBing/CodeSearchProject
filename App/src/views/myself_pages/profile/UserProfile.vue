<template>
    <div class="user-profile-page">
        <PageNavBar title="个人资料" right-text="保存" @click-right="saveProfile" />
        <div class="avatar-section">
            <van-image round width="80px" height="80px" :src="profile.avatar || ''" />
            <span class="change-avatar" @click="changeAvatar">更换头像</span>
        </div>
        <van-cell-group>
            <van-field v-model="profile.username" label="用户名" placeholder="请输入用户名" />
            <van-field v-model="profile.bio" label="个人简介" placeholder="请输入个人简介" type="textarea" rows="3" />
            <van-field v-model="profile.email" label="邮箱" placeholder="请输入邮箱" />
            <van-field v-model="profile.location" label="所在地" placeholder="请输入所在地" />
            <van-field v-model="profile.website" label="个人网站" placeholder="请输入个人网站" />
            <van-field v-model="profile.github" label="GitHub" placeholder="请输入GitHub地址" />
        </van-cell-group>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import { profileApi } from '@/assets/app_request_api.js'
import { getUserId } from '@/assets/local_storage.js'
import PageNavBar from '@/components/PageNavBar.vue'
const profile = ref({ username: '', avatar: '', bio: '', email: '', location: '', website: '', github: '' })
const loadProfile = async () => {
    const data = await profileApi.getProfile(getUserId())
    profile.value = data || {}
}
const saveProfile = async () => {
    await profileApi.updateProfile(profile.value)
    showToast('保存成功')
}
const changeAvatar = () => { showToast('选择头像') }
onMounted(() => { loadProfile() })
</script>

<style scoped>
.user-profile-page { background: #f5f5f5; min-height: 100vh; }
.avatar-section { display: flex; flex-direction: column; align-items: center; padding: 24px; background: #fff; margin-bottom: 8px; }
.change-avatar { margin-top: 12px; color: #1989fa; font-size: 14px; }
</style>
