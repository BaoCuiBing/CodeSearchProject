# 用户资料路由接口文档

## 文件路径
`router/app_profile_router.py`

## 蓝图配置
- **蓝图名称**: `profile`
- **URL前缀**: `/api/profile`

## 接口列表

### 1. 获取用户信息（APP端）
- **路径**: `/api/profile/<user_id>`
- **方法**: `GET`
- **函数名**: `get_user_profile`
- **OpenAPI摘要**: 获取用户个人主页统计数据（跨表聚合计算）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| user_id | int | 用户ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| current_user_id | int | yes | 当前用户ID（用于计算is_followed） | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 用户详情数据 |
| data.user_id | int | 用户ID |
| data.username | string | 用户名 |
| data.avatar | string | 头像URL |
| data.bio | string | 个人简介 |
| data.email | string | 邮箱（脱敏） |
| data.location | string | 所在地 |
| data.website | string | 个人网站 |
| data.github | string | GitHub地址 |
| data.stats | object | 统计数据 |
| data.stats.article_count | int | 发布文章数（动态查询posts表统计） |
| data.stats.question_count | int | 提问数（动态查询posts表统计） |
| data.stats.follower_count | int | 粉丝数（动态查询follows表统计） |
| data.stats.following_count | int | 关注数（动态查询follows表统计） |
| data.stats.like_count | int | 获赞数（动态查询posts表sum聚合like_count） |
| data.stats.view_count | int | 浏览量（动态查询posts表sum聚合） |
| data.created_at | datetime | 注册时间 |
| data.is_followed | bool | 当前用户是否已关注（动态查询follows表） |

#### 请求示例
```
GET /api/profile/1?current_user_id=2
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

---

### 2. 更新个人资料（APP端）
- **路径**: `/api/profile`
- **方法**: `PUT`
- **函数名**: `update_profile`
- **OpenAPI摘要**: 更新当前用户个人资料（UI图13）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| username | string | no | 用户名 | Body (JSON) |
| avatar | string | no | 头像URL（先调用/api/upload/file上传，再填入返回的URL） | Body (JSON) |
| bio | string | no | 个人简介（最多200字） | Body (JSON) |
| email | string | no | 邮箱 | Body (JSON) |
| location | string | no | 所在地 | Body (JSON) |
| website | string | no | 个人网站 | Body (JSON) |
| github | string | no | GitHub地址 | Body (JSON) |

#### 请求示例
```
PUT /api/profile
Content-Type: application/json

{
    "user_id": 1,
    "username": "新用户名",
    "bio": "这是我的个人简介",
    "location": "北京",
    "website": "https://example.com"
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 更新后的用户信息 |
| data.user_id | int | 用户ID |
| data.username | string | 用户名 |
| data.avatar | string | 头像URL |
| data.bio | string | 个人简介 |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "用户名已存在"
}
```

---

### 3. 修改密码（APP端）
- **路径**: `/api/profile/password`
- **方法**: `PUT`
- **函数名**: `change_password`
- **OpenAPI摘要**: 修改登录密码

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| old_password | string | yes | 原密码 | Body (JSON) |
| new_password | string | yes | 新密码（6-20位） | Body (JSON) |

#### 请求示例
```
PUT /api/profile/password
Content-Type: application/json

{
    "user_id": 1,
    "old_password": "old123456",
    "new_password": "new123456"
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "原密码错误"
}
```
