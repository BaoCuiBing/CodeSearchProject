# 管理后台系统设置接口文档

## 文件路径
`router/admin_system_router.py`

## 蓝图配置
- **蓝图名称**: `admin_system`
- **URL前缀**: `/api/admin/system`

## 接口列表

### 1. 获取系统设置（管理端）
- **路径**: `/api/admin/system/settings`
- **方法**: `GET`
- **函数名**: `get_system_settings`
- **OpenAPI摘要**: 获取所有系统设置项（UI图30）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| key | string | no | 设置键筛选 | Query |

#### 请求示例
```
GET /api/admin/system/settings?admin_id=1
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "admin_id不能为空"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": [
        {
            "system_setting_id": 1,
            "key": "site_name",
            "value": "代码搜索社区",
            "description": "站点名称",
            "created_at": "2024-01-01 00:00:00",
            "updated_at": "2024-01-15 10:30:00"
        },
        {
            "system_setting_id": 2,
            "key": "site_description",
            "value": "专业的技术问答和文章分享平台",
            "description": "站点描述",
            "created_at": "2024-01-01 00:00:00",
            "updated_at": "2024-01-15 10:30:00"
        }
    ]
}
```

---

### 2. 更新系统设置（管理端）
- **路径**: `/api/admin/system/settings`
- **方法**: `PUT`
- **函数名**: `update_system_settings`
- **OpenAPI摘要**: 更新系统设置项

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| key | string | yes | 设置键 | Body (JSON) |
| value | string | yes | 设置值 | Body (JSON) |
| description | string | no | 设置说明 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "key": "site_name",
    "value": "代码搜索社区",
    "description": "站点名称"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "设置键不能为空"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "更新成功",
    "data": {
        "system_setting_id": 1,
        "key": "site_name",
        "value": "代码搜索社区",
        "description": "站点名称",
        "created_at": "2024-01-01 00:00:00",
        "updated_at": "2024-01-15 10:30:00"
    }
}
```

---

### 3. 重置设置为默认值（管理端）
- **路径**: `/api/admin/system/settings/reset`
- **方法**: `POST`
- **函数名**: `reset_settings_to_default`
- **OpenAPI摘要**: 重置指定设置键为默认值

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| key | string | yes | 要重置的设置键 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "key": "site_name"
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "设置项不存在"
}
```

---

### 4. 测试邮件发送（管理端）
- **路径**: `/api/admin/system/test-email`
- **方法**: `POST`
- **函数名**: `test_email_config`
- **OpenAPI摘要**: 测试邮件配置是否正确

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| to_email | string | yes | 测试接收邮箱 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "to_email": "test@example.com"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "测试邮件发送成功",
    "data": {
        "success": true,
        "message": "邮件已发送至 test@example.com"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "邮箱格式不正确"
}
```

---

### 5. 清除缓存（管理端）
- **路径**: `/api/admin/system/clear-cache`
- **方法**: `POST`
- **函数名**: `clear_cache`
- **OpenAPI摘要**: 清除系统缓存

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| cache_types | array | no | 缓存类型：all/page/data/session/template，默认all | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "cache_types": ["all"]
}
```

#### 响应示例（失败）
```json
{
    "code": 500,
    "msg": "缓存清除失败"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "缓存清除成功",
    "data": {
        "cleared_types": ["page", "data"],
        "affected_keys": 15
    }
}
```
