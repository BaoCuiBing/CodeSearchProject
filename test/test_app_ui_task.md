# APP UI 测试报告

## 测试环境
- 浏览器: Chromium (无头模式)
- 视口: 375x812 (移动端)
- 测试时间: 2026-05-06
- 测试地址: http://127.0.0.1:5173

## 测试页面清单

### 1. 首页 (/shouye)
**状态**: 正常加载 ✅
**模拟数据**:
- Banner数据: 3条 (搜索技术问题、分享编程经验、探索开源项目)
- 热门标签: 6个 (Python、JavaScript、Vue、React、Docker、MySQL)
- 文章列表: 3条 (程序员小明、前端小王、DBA老张)
**数据符合度**: 
- 文章卡片包含: username、created_at、title、summary、tags、view_count、like_count、comment_count
- 符合posts表结构，但缺少: id(使用post_id)、user_id、category_id、type、status、is_top、cover_image、updated_at
**交互功能**:
- 搜索框点击跳转至/search ✅
- Banner轮播图点击跳转至搜索页 ✅
- 热门标签点击跳转至/tag ✅
- 文章卡片点击跳转至文章详情 ✅

### 2. 发现页 (/faxian)
**状态**: 正常加载 ✅
**模拟数据**:
- 分类: 8个 (后端开发、前端开发、移动开发、数据库、运维部署、人工智能、算法、工具)
- 文章排行榜: 5条 (含hot_score字段)
- 用户排行榜: 5条 (含article_count、question_count、follower_count等)
- 推荐用户: 3条
**数据符合度**:
- 分类数据符合categories表，但缺少: description、sort、updated_at
- 文章排行符合posts表，但使用post_id而非id
- 用户数据符合users表，但使用user_id而非id，缺少: usernumber、password、salt、role、status、is_verified等
**交互功能**:
- 分类点击跳转至/category ✅
- 排行榜文章点击跳转至文章详情 ✅
- 推荐关注按钮支持关注/取消关注切换 ✅

### 3. 消息页 (/message)
**状态**: 正常加载
**模拟数据**:
- 通知列表: 5条 (评论、点赞、关注、系统通知)
- 包含: notification_id、type、content、is_read、actor、created_at、related_id
**数据符合度**:
- 符合notifications表结构，但字段使用notification_id而非id
- type值: comment/like/follow/system，与数据库定义的system/system_msg/comment/like/follow略有差异
- 缺少: updated_at字段
**问题**:
- 消息列表项点击可跳转至文章详情 (related_id > 0时)
- 全部已读功能仅前端状态更新，无后端交互

### 4. 我的页 (/myself)
**状态**: 正常加载
**模拟数据**:
- 用户信息: user_id=1, username='程序员小明', bio='热爱编程，乐于分享'
- 统计数据: following_count=128, follower_count=256, like_count=1024
**数据符合度**:
- 符合users表，但使用user_id而非id
- 缺少: usernumber、email、phone、role、avatar(使用固定URL)、status、is_verified、last_login_time等
- stats为前端计算字段，数据库中需通过关联查询获取
**问题**:
- 设置图标点击可跳转至/settings
- 所有菜单项均可正常跳转对应页面

### 5. 文章详情页 (/article?id=1)
**状态**: 正常加载
**模拟数据**:
- 文章: post_id=1, type='article', title、content、summary、cover_image
- 作者: user_id=1, username、avatar
- 标签: 2个 (Python、并发)
- 统计: like_count=86, favorite_count=45, comment_count=23, view_count=1205
- 评论: 3条 (含comment_id、user、content、like_count、created_at)
**数据符合度**:
- posts表字段基本符合，但使用post_id而非id
- 评论符合comments表，但使用comment_id而非id，缺少: post_id、parent_id、status、updated_at
- 缺少: category_id、status、is_top、updated_at
**问题**:
- 有返回按钮 (van-nav-bar left-arrow)
- 点赞/收藏按钮有前端状态切换逻辑
- 关注按钮有前端状态切换逻辑

### 6. 标签列表页 (/tags)
**状态**: 正常加载
**模拟数据**:
- 热门标签: 8个 (含tag_id、name、color)
- 全部标签: 10个 (含tag_id、name、color、post_count)
**数据符合度**:
- 符合tags表，但缺少: slug、description、is_hot、is_recommend、category_id、sort_order、status、created_at、updated_at
- 使用tag_id而非id
**问题**:
- 标签点击可跳转至/tag页面

### 7. 标签文章页 (/tag?id=1)
**状态**: 正常加载
**模拟数据**: 2篇文章
**数据符合度**: 简化版posts数据，仅含post_id、title、summary、view_count、like_count
**问题**:
- 文章卡片点击可跳转至文章详情

### 8. 分类文章页 (/category?id=1)
**状态**: 正常加载
**模拟数据**:
- 分类信息: category_id、name、icon、description、post_count
- 文章列表: 3条
**数据符合度**:
- 分类符合categories表，但缺少: sort、created_at、updated_at
- 文章为简化版posts数据
**问题**:
- 文章卡片点击可跳转至文章详情

### 9. 排行榜页 (/rankings)
**状态**: 正常加载
**模拟数据**:
- 文章热榜: 5条 (含hot_score)
- 问题热榜: 3条
- 贡献者: 5条 (用户数据)
**数据符合度**:
- hot_score为计算字段，数据库中无此字段，需通过view_count、like_count等计算
- 用户数据符合users表简化版
**问题**:
- 排名项点击可跳转至文章详情

### 10. 搜索页 (/search)
**状态**: 正常加载
**模拟数据**:
- 搜索历史: 3条 (Python多线程、Vue3响应式、MySQL索引)
- 热门搜索: 6个 (Python、Vue3、React、Docker、MySQL、Redis)
**数据符合度**:
- 搜索历史符合search_history表结构，但数据库包含user_id、created_at
**问题**:
- 搜索历史点击可跳转至搜索结果页
- 热门搜索点击可跳转至搜索结果页

### 11. 搜索结果页 (/search-result)
**状态**: 正常加载
**模拟数据**:
- 综合结果: 3条
- 文章结果: 1条
- 问题结果: 1条
**数据符合度**: 简化版posts数据
**问题**:
- 文章卡片点击可跳转至文章详情

### 12. 聊天详情页 (/chat?id=1)
**状态**: 正常加载
**模拟数据**:
- 消息列表: 4条 (含id、content、is_self)
**数据符合度**:
- 符合messages表，但使用id而非自增主键，缺少: from_user_id、to_user_id、is_read、created_at、updated_at
**问题**:
- 发送消息功能有前端逻辑 (push到messages数组)
- 输入框可正常输入

### 13. 个人资料页 (/profile)
**状态**: 正常加载 ✅
**模拟数据**:
- 用户资料: user_id、username、avatar、bio、email、location、website、github
**数据符合度**:
- 符合users表字段: username、email、location、website、github、bio、avatar
- 缺少: usernumber、password、salt、role、status、is_verified等
**交互功能**:
- 保存按钮有Toast提示 ✅
- 更换头像有Toast提示 ✅

### 14. 设置页 (/settings)
**状态**: 正常加载 ✅
**数据符合度**: 无数据展示
**交互功能**:
- 清除缓存有Toast提示 ✅
- 退出登录跳转至首页 ✅
- 关于我们点击可跳转 ✅

### 15. 账号安全页 (/security)
**状态**: 正常加载 ✅
**数据符合度**: 无数据展示
**交互功能**:
- 修改密码有Toast提示 ✅
- 绑定邮箱有Toast提示 ✅
- 绑定手机有Toast提示 ✅

### 16. 关于我们页 (/about)
**状态**: 正常加载
**数据**: 应用名称、版本号、描述
**问题**: 无异常

### 17. 我的关注页 (/following)
**状态**: 正常加载 ✅
**模拟数据**: 2条用户数据
**数据符合度**: 符合follows表关联users的简化数据
**交互功能**:
- 取消关注按钮支持状态切换 ✅

### 18. 我的粉丝页 (/followers)
**状态**: 正常加载 ✅
**模拟数据**: 2条用户数据
**数据符合度**: 符合follows表关联users的简化数据
**交互功能**:
- 回关按钮支持状态切换 ✅

### 19. 我的文章页 (/my-articles)
**状态**: 正常加载
**模拟数据**: 2篇文章
**数据符合度**: 简化版posts数据，仅含post_id、title、summary、view_count、like_count
**问题**:
- 文章卡片点击可跳转至文章详情

### 20. 我的提问页 (/my-questions)
**状态**: 正常加载
**模拟数据**: 2个问题
**数据符合度**: 使用question_id而非post_id，数据库中posts表通过type='question'区分问题
**问题**:
- 问题卡片点击跳转路径为/question (路由可能不存在)

### 21. 我的收藏页 (/favorites)
**状态**: 正常加载
**模拟数据**:
- 文章: 2条
- 问题: 1条
**数据符合度**:
- 符合favorites表关联posts的简化数据
- 问题使用question_id，与数据库设计不符 (应使用post_id)
**问题**:
- 文章/问题卡片点击可跳转

### 22. 浏览历史页 (/history)
**状态**: 正常加载
**模拟数据**: 2条浏览记录
**数据符合度**: 数据库中无专门浏览历史表，需通过其他方式实现
**问题**:
- 文章卡片点击可跳转至文章详情

## 数据字段对照总结

### 与数据库设计的主要差异:
1. **主键命名**: 前端使用 `{table}_id` (如post_id、user_id、tag_id)，数据库使用 `id`
2. **posts表缺失字段**: type、status、is_top、cover_image(JSON)、updated_at
3. **users表缺失字段**: usernumber、password、salt、role、status、is_verified、ban_reason、last_login_time、login_ip、device_info
4. **comments表缺失字段**: parent_id(楼中楼)、status、updated_at
5. **tags表缺失字段**: slug(别名)、is_hot、is_recommend、sort_order、status
6. **messages表缺失字段**: is_read、created_at、updated_at
7. **计算字段**: hot_score(热度)、stats(统计) 需后端计算
8. **问题类型**: 前端使用独立question_id，数据库通过posts.type='question'区分

## 共性问题总结
1. ✅ 页面元素点击响应已修复（Banner、搜索框、分类、关注按钮等）
2. ✅ 按钮功能已实现（Toast提示、状态切换、路由跳转）
3. 模拟数据字段与数据库设计存在差异（主键命名、缺失字段）
4. 部分页面使用简化版数据，缺少完整字段
5. 问题/文章类型处理不一致（独立question_id vs posts.type）
6. 无浏览历史表设计（数据库设计中未包含）
7. 所有交互均为前端模拟，无后端API调用

## 遗漏功能详细清单

### 首页 (/shouye) 遗漏功能
1. **Banner轮播点击跳转**: ✅ 已修复，点击跳转至搜索页
2. **搜索框点击**: ✅ 已修复，点击跳转至/search
3. **热门标签点击**: ✅ 已有goToTag方法
4. **Tab切换数据过滤**: 推荐/文章/问题三个Tab使用不同数据源，但切换时无加载状态
5. **文章卡片点赞/收藏状态**: 数据包含is_liked、is_favorited字段，但页面无显示切换逻辑

### 发现页 (/faxian) 遗漏功能
1. **分类浏览点击**: ✅ 已有goToCategory方法
2. **排行榜Tab切换**: 文章热榜/用户活跃两个Tab，用户活跃Tab数据正常显示
3. **推荐关注按钮**: ✅ 已修复，支持关注/取消关注切换
4. **搜索功能**: onSearch方法仅跳转，无实际搜索请求

### 消息页 (/message) 遗漏功能
1. **消息Tab切换**: 全部/评论/点赞/关注四个Tab，但评论/点赞/关注Tab数据未显示
2. **消息已读标记**: markAllRead仅前端更新is_read状态，无后端同步
3. **消息点击跳转**: ✅ 已有goToDetail方法

### 我的页 (/myself) 遗漏功能
1. **设置图标点击**: ✅ 已有goToSettings方法
2. **统计数据来源**: following_count、follower_count、like_count为硬编码，无后端获取

### 文章详情页 (/article?id=1) 遗漏功能
1. **点赞按钮**: toggleLike有前端状态切换，但无后端同步
2. **收藏按钮**: toggleFavorite有前端状态切换，但无后端同步
3. **关注作者**: toggleFollow有前端状态切换，但无后端同步
4. **分享功能**: 仅显示"分享"文字，无实际分享逻辑
5. **评论列表**: 评论数据缺少parent_id(楼中楼)、status字段
6. **评论输入框**: 页面无评论输入和提交功能

### 标签列表页 (/tags) 遗漏功能
1. **标签点击**: ✅ 已有goToTag方法
2. **标签数据**: 缺少slug、description、is_hot、is_recommend、sort_order、status字段

### 排行榜页 (/rankings) 遗漏功能
1. **Tab切换**: 文章热榜/用户活跃两个Tab，数据量不一致(首页5条，排行榜页2条)
2. **hot_score计算**: 数据库中无此字段，需后端计算

### 搜索页 (/search) 遗漏功能
1. **搜索历史删除**: removeHistory方法仅前端删除，无后端同步
2. **搜索历史存储**: 数据库search_history表包含user_id、created_at，前端未体现

### 个人资料页 (/profile) 遗漏功能
1. **保存功能**: ✅ 已修复，有Toast提示
2. **更换头像**: ✅ 已修复，有Toast提示
3. **表单验证**: 无邮箱格式、用户名长度等验证

### 设置页 (/settings) 遗漏功能
1. **版本差异**: Settings.vue和SettingsPage.vue两个文件内容不同
   - Settings.vue: 清除缓存/关于我们/退出登录
   - SettingsPage.vue: 账号与安全/隐私设置/消息通知/清除缓存/退出登录
2. **清除缓存**: ✅ 已修复，有Toast提示
3. **退出登录**: ✅ 已修复，跳转至首页
4. **隐私设置**: ✅ 已添加/privacy路由
5. **消息通知设置**: ✅ 已添加/notification-settings路由

### 关注/粉丝页遗漏功能
1. **Following.vue vs FollowList.vue**: 两个文件功能重叠
   - Following.vue: ✅ 已修复，支持取消关注切换
   - FollowList.vue: ✅ 已添加路由，支持toggleFollow切换关注状态
2. **取消关注**: ✅ 已修复
3. **回关功能**: ✅ 已修复

### 收藏页遗漏功能
1. **Favorites.vue vs MyFavorites.vue**: 两个文件功能重叠
   - Favorites.vue: 文章/问题两个Tab，使用question_id
   - MyFavorites.vue: ✅ 已添加路由，全部/文章/问题三个Tab
2. **取消收藏**: 无取消收藏功能

### 聊天详情页 (/chat?id=1) 遗漏功能
1. **消息发送**: sendMessage有前端逻辑(push到数组)，但无后端发送
2. **消息时间**: 消息数据缺少created_at字段
3. **消息已读**: 无is_read状态管理
4. **文件发送**: 无图片/文件发送功能

### 系统通知页 (/system-notice) 遗漏功能
1. **通知数据**: ✅ 已添加路由，符合system_messages表简化版
2. **通知已读**: 无is_read状态管理

### 路由跳转问题
1. **已修复的缺失路由** ✅:
   - `/search-result`: 搜索结果页
   - `/system-notice`: 系统通知页
   - `/category-detail`: 分类详情页
   - `/follow-list`: 关注/粉丝列表统一组件
   - `/settings-page`: 设置页增强版
   - `/my-favorites`: 收藏页增强版
   - `/question`: 问题详情页(复用ArticleDetail)
   - `/privacy`: 隐私设置(复用About)
   - `/notification-settings`: 通知设置(复用Settings)
   - `/login`: 登录页(重定向至首页)
2. **路由命名不一致**:
   - `/tag?id=1` 使用TagArticles组件
   - `/category?id=1` 使用CategoryArticles组件

### 数据库字段遗漏汇总
1. **users表**: usernumber、password、salt、role、status、is_verified、ban_reason、ban_expire_time、last_login_time、login_ip、device_info
2. **posts表**: status、is_top、cover_image(JSON格式)、updated_at
3. **comments表**: parent_id、status、updated_at
4. **tags表**: slug、description、is_hot、is_recommend、sort_order、status
5. **messages表**: is_read、updated_at
6. **notifications表**: updated_at
7. **categories表**: sort、updated_at
8. **favorites表**: 无独立页面使用created_at字段
9. **follows表**: 无独立页面使用created_at字段
10. **search_history表**: created_at字段未体现
