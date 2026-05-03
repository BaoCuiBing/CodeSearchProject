# 管理后台登录认证接口文档

## 文件路径
`router/admin_auth_router.py`

## 蓝图配置
- **蓝图名称**: `admin_auth`
- **URL前缀**: `/api/admin/auth`

## 接口列表

### 1. 管理员登录（管理端）
- **路径**: `/api/admin/auth/login`
- **方法**: `POST`
- **函数名**: `admin_login`
- **OpenAPI摘要**: 管理员登录（UI图23）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| usernumber | string | yes | 管理员账号 | Body (JSON) |
| password | string | yes | 密码 | Body (JSON) |

#### 请求示例
```json
{
    "usernumber": "admin",
    "password": "admin123"
}
```

#### 响应格式（成功）
```json
{
    "code": 200,
    "msg": "登录成功",
    "data": {
        "admin_id": 1,
        "username": "超级管理员",
        "role": "admin",
        "avatar": "/static/uploads/admin_avatar.jpg"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "账号或密码错误"
}
```

#### 响应示例（失败：无管理员权限/账号被封禁）
```json
{
    "code": 403,
    "msg": "权限不足"
}
```

---

### 2. 获取当前管理员信息（管理端）
- **路径**: `/api/admin/auth/me`
- **方法**: `GET`
- **函数名**: `get_current_admin`
- **OpenAPI摘要**: 获取当前登录的管理员信息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "admin_id": 1,
        "username": "超级管理员",
        "role": "admin",
        "avatar": "/static/uploads/admin_avatar.jpg",
        "last_login_time": "2024-01-15 10:30:00"
    }
}
```

---

### 3. 修改管理员密码（管理端）
- **路径**: `/api/admin/auth/change-password`
- **方法**: `PUT`
- **函数名**: `change_admin_password`
- **OpenAPI摘要**: 修改当前管理员登录密码（UI图34）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| old_password | string | yes | 当前密码 | Body (JSON) |
| new_password | string | yes | 新密码（8位以上） | Body (JSON) |
| confirm_password | string | yes | 确认新密码 | Body (JSON) |
