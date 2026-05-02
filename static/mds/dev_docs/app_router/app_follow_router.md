# 关注路由接口文档

## 文件路径
`router/app_follow_router.py`

## 蓝图配置
- **蓝图名称**: `follow`
- **URL前缀**: `/api/follow`

## 接口列表

### 1. 获取我关注的用户列表（APP端）
- **路径**: `/api/follow/following`
- **方法**: `GET`
- **函数名**: `get_my_following_users`
- **OpenAPI摘要**: 获取当前用户关注的用户列表（UI图18）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| follower_id | int | yes | 当前用户ID（follows.follower_id） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 关注列表数据 |
| data.list | array | 关注列表 |
| data.total | int | 总数 |
| data.list[].user_id | int | 用户ID |
| data.list[].username | string | 用户名 |
| data.list[].avatar | string | 头像URL |
| data.list[].bio | string | 个人简介 |
| data.list[].is_mutual | bool | 是否互相关注 |
| data.list[].created_at | datetime | 关注时间 |

#### 请求示例
```
GET /api/follow/following?follower_id=1&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "follower_id不能为空"
}
```

---

### 2. 获取我的粉丝列表（APP端）
- **路径**: `/api/follow/followers`
- **方法**: `GET`
- **函数名**: `get_my_followers`
- **OpenAPI摘要**: 获取当前用户的粉丝列表（UI图18）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| following_id | int | yes | 当前用户ID（follows.following_id） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 粉丝列表数据 |
| data.list | array | 粉丝列表 |
| data.total | int | 总数 |
| data.list[].user_id | int | 用户ID |
| data.list[].username | string | 用户名 |
| data.list[].avatar | string | 头像URL |
| data.list[].bio | string | 个人简介 |
| data.list[].is_followed_back | bool | 是否已回关 |
| data.list[].created_at | datetime | 关注时间 |

#### 请求示例
```
GET /api/follow/followers?following_id=1&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "following_id不能为空"
}
```

---

### 3. 关注/取消关注用户（APP端）
- **路径**: `/api/follow/user`
- **方法**: `POST`
- **函数名**: `toggle_follow_user`
- **OpenAPI摘要**: 关注或取消关注用户（UI图18）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| follower_id | int | yes | 当前用户ID（follows.follower_id） | Body (JSON) |
| following_id | int | yes | 目标用户ID（follows.following_id） | Body (JSON) |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 操作结果 |
| data.is_followed | bool | 是否已关注 |
| data.follower_count | int | 粉丝数（动态查询follows表统计） |

#### 请求示例
```
POST /api/follow/user
Content-Type: application/json

{
    "follower_id": 1,
    "following_id": 5
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "不能关注自己"
}
```

---

### 4. 获取用户关注列表（APP端）
- **路径**: `/api/follow/user/<follower_id>/following`
- **方法**: `GET`
- **函数名**: `get_following_list`
- **OpenAPI摘要**: 获取指定用户的关注列表（UI图18）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| follower_id | int | 用户ID（follows.follower_id） |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID（用于计算is_mutual） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 关注列表数据 |
| data.list | array | 关注列表 |
| data.total | int | 总数 |
| data.list[].user_id | int | 用户ID |
| data.list[].username | string | 用户名 |
| data.list[].avatar | string | 头像URL |
| data.list[].bio | string | 个人简介 |
| data.list[].is_mutual | bool | 是否互相关注 |
| data.list[].created_at | datetime | 关注时间 |

#### 请求示例
```
GET /api/follow/user/1/following?user_id=2&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

---

### 5. 获取用户粉丝列表（APP端）
- **路径**: `/api/follow/user/<following_id>/followers`
- **方法**: `GET`
- **函数名**: `get_followers_list`
- **OpenAPI摘要**: 获取指定用户的粉丝列表（UI图18）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| following_id | int | 用户ID（follows.following_id） |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID（用于计算is_followed_back） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 粉丝列表数据 |
| data.list | array | 粉丝列表 |
| data.total | int | 总数 |
| data.list[].user_id | int | 用户ID |
| data.list[].username | string | 用户名 |
| data.list[].avatar | string | 头像URL |
| data.list[].bio | string | 个人简介 |
| data.list[].is_followed_back | bool | 是否已回关 |
| data.list[].created_at | datetime | 关注时间 |

#### 请求示例
```
GET /api/follow/user/1/followers?user_id=2&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```
