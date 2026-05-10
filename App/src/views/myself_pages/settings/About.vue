<template>
    <div class="about-page">
        <PageNavBar title="关于我们" />
        <div class="about-content">
            <van-image width="80px" height="80px" src="/imgs/bo_luo_tb.png" />
            <h3>代码搜索社区</h3>
            <p>版本 1.0.0</p>
            <p>代码Search与内容分享平台</p>
            <van-cell-group class="info-group">
                <van-cell v-for="item in infoList" :key="item.title" :title="item.title" :value="item.title === '用户协议' || item.title === '隐私政策' ? '' : item.value" is-link @click="handleInfoClick(item)" />
            </van-cell-group>
            <div class="tech-stack">
                <p class="tech-title">技术栈</p>
                <div class="tech-tags">
                    <van-tag v-for="(tech, idx) in techStack" :key="tech.name" :color="getRandomColor(idx)" class="tech-tag" @click="openLink(tech.url)">{{ tech.name }}</van-tag>
                </div>
            </div>
        </div>
        <van-dialog v-model:show="dialogVisible" :title="dialogTitle" @confirm="dialogVisible = false">
            <div class="dialog-content">{{ dialogContent }}</div>
        </van-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageNavBar from '@/components/PageNavBar.vue'
import { systemApi } from '@/assets/app_request_api.js'
const infoList = ref([])
const techStack = ref([])
const protocolMap = ref({})
const dialogVisible = ref(false)
const dialogTitle = ref('')
const dialogContent = ref('')
const colorPool = ['#1989fa', '#07c160', '#ff976a', '#ee0a24', '#7232dd', '#f44336', '#2196f3', '#4caf50', '#ff9800', '#9c27b0']
const getRandomColor = (idx) => colorPool[idx % colorPool.length]
const openLink = (url) => { if (url) { window.open(url, '_blank') } }
const handleInfoClick = (item) => {
    if (item.title === '用户协议' || item.title === '隐私政策') {
        dialogTitle.value = item.title
        dialogContent.value = protocolMap.value[item.title] || '暂无内容'
        dialogVisible.value = true
    }
}
onMounted(async () => {
    try {
        const data = await systemApi.getAboutConfig()
        if (data) {
            infoList.value = data.info_list || []
            techStack.value = data.tech_stack || []
            infoList.value.forEach(item => { protocolMap.value[item.title] = item.value })
        }
    } catch (e) {}
})
</script>

<style scoped>
.about-page { background: #f5f5f5; min-height: 100vh; }
.about-content { width: 90%; margin: 0 auto; display: flex; flex-direction: column; align-items: center; padding: 40px 16px; }
.about-content h3 { margin: 16px 0 4px; font-size: 22px; color: #333; }
.about-content p { margin: 4px 0; font-size: 14px; color: #999; }
.info-group { width: 100%; margin-top: 24px; }
.tech-stack { margin-top: 24px; text-align: center; }
.tech-title { font-size: 14px; color: #666; margin-bottom: 12px; }
.tech-tags { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
.tech-tag { margin: 4px; padding: 4px 12px; cursor: pointer; color: #fff; }
.dialog-content { padding: 16px; text-align: left; white-space: pre-wrap; font-size: 14px; line-height: 1.6; color: #333; max-height: 60vh; overflow-y: auto; }
</style>