# 任务：为Vue页面加入加载状态 + 静态数据改真实API + 功能完善

> **状态：✅ 全部完成**

## 一、删除文件（3个）✅

| 文件 | 原因 | 状态 |
|------|------|------|
| `App/src/views/myself_pages/content/History.vue` | 后端无浏览历史API | ✅ 已删除 |
| `App/src/views/myself_pages/content/Favorites.vue` | 与 MyFavorites.vue 重复 | ✅ 已删除 |
| `App/src/views/faxian_pages/rankings/RankingList.vue` | 与 Rankings.vue 重复 | ✅ 已删除 |

## 二、修改 MySelf.vue ✅

移除"浏览历史"菜单项及 `goToHistory` 相关代码，加入 loading/error/重试

## 三、后端路由完善 ✅

### 3.1 app_profile_router.py ✅
- GET `/api/profile/<user_id>` 响应中增加 `phone` 字段
- PUT `/api/profile` 请求参数中增加 `phone` 字段支持

### 3.2 文档更新
- 更新 `static/mds/router_dev_docs/app_router/app_profile_router.md`

## 四、静态数据改真实API（2个）✅

### 4.1 MyFavorites.vue ✅
- 改用 `favoriteApi.getList()` 获取数据
- 加入 loading/error/重试

### 4.2 FollowList.vue ✅
- 根据 `route.query.type` 判断调用 `followApi.getFollowing()` 或 `followApi.getFollowers()`
- 加入 loading/error/重试

## 五、Security.vue 功能完善 ✅

### 5.1 修改密码 ✅
- 自定义弹窗：输入旧密码、新密码、确认新密码
- 调用 `profileApi.changePassword()`

### 5.2 绑定邮箱 ✅
- 自定义弹窗：输入邮箱
- 调用 `profileApi.updateProfile({ email })`

### 5.3 绑定手机 ✅
- 自定义弹窗：输入手机号
- 调用 `profileApi.updateProfile({ phone })`

## 六、需加 loading/error/重试 的页面（19个）✅

| 页面 | 数据接口 | 状态 |
|------|----------|------|
| Main.vue | banners/hotTags/recommendPosts（初始），articlePosts/questionPosts（仅error） | ✅ |
| FaXian.vue | categories/rankings/recommendUsers | ✅ |
| Message.vue | notifications/conversations | ✅ |
| ArticleDetail.vue | article/comments | ✅ |
| Search.vue | history/hotSearches | ✅ |
| SearchResult.vue | search results | ✅ |
| TagList.vue | hotTags/allTags | ✅ |
| TagArticles.vue | articles | ✅ |
| CategoryDetail.vue | category/posts | ✅ |
| CategoryArticles.vue | articles | ✅ |
| Rankings.vue | rankings | ✅ |
| SystemNotice.vue | notices | ✅ |
| ChatDetail.vue | messages | ✅ |
| MyArticles.vue | articles | ✅ |
| MyQuestions.vue | questions | ✅ |
| MyFavorites.vue | favorites | ✅ |
| Following.vue | followingList | ✅ |
| Followers.vue | followersList | ✅ |
| FollowList.vue | users | ✅ |
| UserProfile.vue | profile | ✅ |
| MySelf.vue | userProfile | ✅ |
| PostEdit.vue | 发布按钮 loading + 错误处理 | ✅ |

## 七、不处理的页面（5个）

Login、Register、Settings、SettingsPage、About — 表单页或静态页，无数据加载