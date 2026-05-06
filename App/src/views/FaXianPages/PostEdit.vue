<template>
    <div class="post-edit-page">
        <PageNavBar title="发布内容" right-text="发布" @click-right="publishPost" />
        <div class="edit-form">
            <van-field v-model="postForm.title" placeholder="请输入标题（最多50字）" maxlength="50" />
            <div class="type-selector">
                <van-radio-group v-model="postForm.type" direction="horizontal">
                    <van-radio name="article">文章</van-radio>
                    <van-radio name="question">问题</van-radio>
                </van-radio-group>
            </div>
            <div class="category-selector">
                <van-field v-model="postForm.category_name" readonly is-link placeholder="选择分类" @click="showCategoryPicker = true" />
                <van-popup v-model:show="showCategoryPicker" position="bottom" round>
                    <van-picker :columns="categoryColumns" @confirm="onCategoryConfirm" @cancel="showCategoryPicker = false" />
                </van-popup>
            </div>
            <div class="tag-selector">
                <van-field v-model="tagInput" placeholder="添加标签（回车确认）" @keyup.enter="addTag" />
                <div class="tag-list">
                    <van-tag v-for="(tag, index) in postForm.tags" :key="index" closeable size="medium" type="primary" @close="removeTag(index)">{{ tag }}</van-tag>
                </div>
            </div>
            <div class="editor-wrapper">
                <textarea ref="editorRef"></textarea>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'
import EasyMDE from 'easymde'
import PageNavBar from '@/components/PageNavBar.vue'
const router = useRouter()
const editorRef = ref(null)
const showCategoryPicker = ref(false)
const tagInput = ref('')
let easyMDE = null
const categoryColumns = [
    { text: '后端开发', value: 1 },
    { text: '前端开发', value: 2 },
    { text: '移动开发', value: 3 },
    { text: '数据库', value: 4 },
    { text: '运维部署', value: 5 },
    { text: '人工智能', value: 6 },
    { text: '算法', value: 7 },
    { text: '工具', value: 8 }
]
const postForm = ref({
    title: '',
    type: 'article',
    category_id: null,
    category_name: '',
    tags: [],
    content: ''
})
const mockDrafts = ref([
    { post_id: 1, title: 'Python多线程实战', type: 'article', category_id: 1, category_name: '后端开发', tags: ['Python', '并发'], content: '## Python多线程实战\n\n本文详细介绍Python多线程的使用方法...', created_at: '2025-05-05 10:30:00' },
    { post_id: 2, title: 'Vue3组合式API入门', type: 'article', category_id: 2, category_name: '前端开发', tags: ['Vue', '前端'], content: '## Vue3组合式API\n\n组合式API是Vue3的重要特性...', created_at: '2025-05-04 14:20:00' }
])
onMounted(() => {
    nextTick(() => {
        easyMDE = new EasyMDE({
            element: editorRef.value,
            placeholder: '请输入内容，支持Markdown语法...',
            spellChecker: false,
            autoDownloadFontAwesome: false,
            status: ['lines', 'words', 'cursor'],
            toolbar: ['bold', 'italic', 'heading', '|', 'quote', 'unordered-list', 'ordered-list', '|', 'link', 'image', '|', 'preview', 'side-by-side', 'fullscreen', '|', 'guide']
        })
        easyMDE.codemirror.on('change', () => { postForm.value.content = easyMDE.value() })
    })
})
const onCategoryConfirm = ({ selectedOptions }) => {
    postForm.value.category_id = selectedOptions[0].value
    postForm.value.category_name = selectedOptions[0].text
    showCategoryPicker.value = false
}
const addTag = () => {
    const tag = tagInput.value.trim()
    if (tag && !postForm.value.tags.includes(tag) && postForm.value.tags.length < 5) {
        postForm.value.tags.push(tag)
    }
    tagInput.value = ''
}
const removeTag = (index) => { postForm.value.tags.splice(index, 1) }
const publishPost = () => {
    if (!postForm.value.title.trim()) { showToast('请输入标题'); return }
    if (!postForm.value.category_id) { showToast('请选择分类'); return }
    if (!postForm.value.content.trim()) { showToast('请输入内容'); return }
    const newPost = {
        post_id: Date.now(),
        title: postForm.value.title,
        type: postForm.value.type,
        category_id: postForm.value.category_id,
        category_name: postForm.value.category_name,
        tags: [...postForm.value.tags],
        content: postForm.value.content,
        author: { user_id: 1, username: '程序员小明', avatar: 'https://img.yzcdn.cn/vant/cat.jpeg' },
        view_count: 0,
        like_count: 0,
        comment_count: 0,
        favorite_count: 0,
        created_at: new Date().toLocaleString(),
        hot_score: 0
    }
    showSuccessToast('发布成功')
    setTimeout(() => { router.back() }, 1000)
}
</script>

<style scoped>
.post-edit-page { background: #f5f5f5; min-height: 100vh; }
.edit-form { padding: 0; }
.type-selector { padding: 12px 16px; background: #fff; border-bottom: 1px solid #f0f0f0; }
.category-selector { background: #fff; }
.tag-selector { background: #fff; padding-bottom: 12px; }
.tag-list { display: flex; flex-wrap: wrap; gap: 8px; padding: 0 16px 8px; }
.editor-wrapper { padding: 0; }
.editor-wrapper :deep(.EasyMDEContainer) { border: none; }
.editor-wrapper :deep(.editor-toolbar) { border: none; border-bottom: 1px solid #f0f0f0; }
.editor-wrapper :deep(.CodeMirror) { border: none; min-height: 300px; }
</style>
