# 管理后台主页接口文档

## 文件路径
`router/admin_view_router.py`

## 蓝图配置
- **蓝图名称**: `admin_view`
- **URL前缀**: 无（根路由）

## 接口列表

### 1. 管理后台登录页（管理端）
- **路径**: `/admin/login`
- **方法**: `GET`
- **函数名**: `admin_login_page`
- **描述**: 返回管理后台登录页面HTML（UI图23）

#### 请求参数
无

#### 请求示例
```
GET /admin/login
```

#### 响应格式
- **类型**: HTML

---

### 2. 管理后台首页/仪表盘（管理端）
- **路径**: `/admin`
- **方法**: `GET`
- **函数名**: `admin_dashboard_page`
- **描述**: 返回管理后台首页HTML，包含数据概览、快捷操作、最近动态等（UI图23）

#### 请求参数
无

#### 请求示例
```
GET /admin
```

#### 响应格式
- **类型**: HTML

---

### 3. 管理后台仪表盘（管理端）
- **路径**: `/admin/dashboard`
- **方法**: `GET`
- **函数名**: `admin_dashboard_page`
- **描述**: 返回管理后台仪表盘页面HTML，包含数据概览、快捷操作、最近动态等

#### 请求参数
无

#### 请求示例
```
GET /admin/dashboard
```

#### 响应格式
- **类型**: HTML

---

### 4. 用户管理页（管理端）
- **路径**: `/admin/users`
- **方法**: `GET`
- **函数名**: `admin_users_page`
- **描述**: 返回用户管理页面HTML，包含用户列表、搜索筛选、批量操作等功能（UI图24）

#### 请求参数
无

#### 请求示例
```
GET /admin/users
```

#### 响应格式
- **类型**: HTML

---

### 5. 文章管理页（文章列表）（管理端）
- **路径**: `/admin/articles`
- **方法**: `GET`
- **函数名**: `admin_articles_page`
- **描述**: 返回文章/问题管理页面HTML（UI图25）

#### 请求参数
无

#### 请求示例
```
GET /admin/articles
```

#### 响应格式
- **类型**: HTML

---

### 6. 文章管理页（文章详情）（管理端）
- **路径**: `/admin/article/<post_id>`
- **方法**: `GET`
- **函数名**: `admin_article_detail_page`
- **描述**: 返回文章详情编辑页面HTML（UI图26）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章ID |

#### 请求示例
```
GET /admin/article/1
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

#### 响应格式
- **类型**: HTML

---

### 7. 标签管理页（管理端）
- **路径**: `/admin/tags`
- **方法**: `GET`
- **函数名**: `admin_tags_page`
- **描述**: 返回标签管理页面HTML（UI图27）

#### 请求参数
无

#### 请求示例
```
GET /admin/tags
```

#### 响应格式
- **类型**: HTML

---

### 8. 评论管理页（管理端）
- **路径**: `/admin/comments`
- **方法**: `GET`
- **函数名**: `admin_comments_page`
- **描述**: 返回评论管理页面HTML（UI图28）

#### 请求参数
无

#### 请求示例
```
GET /admin/comments
```

#### 响应格式
- **类型**: HTML

---

### 9. 消息管理页（管理端）
- **路径**: `/admin/messages`
- **方法**: `GET`
- **函数名**: `admin_messages_page`
- **描述**: 返回消息通知管理页面HTML（UI图29）

#### 请求参数
无

#### 请求示例
```
GET /admin/messages
```

#### 响应格式
- **类型**: HTML

---

### 10. 系统设置页（管理端）
- **路径**: `/admin/settings`
- **方法**: `GET`
- **函数名**: `admin_settings_page`
- **描述**: 返回系统设置页面HTML（UI图30）

#### 请求参数
无

#### 请求示例
```
GET /admin/settings
```

#### 响应格式
- **类型**: HTML

---

### 11. 数据统计页（管理端）
- **路径**: `/admin/stats`
- **方法**: `GET`
- **函数名**: `admin_stats_page`
- **描述**: 返回数据统计分析页面HTML（UI图31）

#### 请求参数
无

#### 请求示例
```
GET /admin/stats
```

#### 响应格式
- **类型**: HTML

---

### 12. 文件管理页（管理端）
- **路径**: `/admin/files`
- **方法**: `GET`
- **函数名**: `admin_files_page`
- **描述**: 返回文件管理页面HTML（UI图32）

#### 请求参数
无

#### 请求示例
```
GET /admin/files
```

#### 响应格式
- **类型**: HTML

---

### 13. 管理员个人中心页（管理端）
- **路径**: `/admin/profile`
- **方法**: `GET`
- **函数名**: `admin_profile_page`
- **描述**: 返回管理员个人信息和修改密码页面HTML（UI图34）

#### 请求参数
无

#### 请求示例
```
GET /admin/profile
```

#### 响应格式
- **类型**: HTML

---

### 14. 对话框页面（管理端）
- **路径**: `/admin/dialogs/<path:path>`
- **方法**: `GET`
- **函数名**: `admin_dialogs_page`
- **描述**: 返回管理后台各对话框（弹出层）HTML页面

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| path | string | 对话框模板路径，如user_edit.html、article_create.html等 |

#### 请求参数
无

#### 请求示例
```
GET /admin/dialogs/user_edit.html
```

#### 响应格式
- **类型**: HTML
