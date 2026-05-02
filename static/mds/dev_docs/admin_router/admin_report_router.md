# 管理后台举报管理接口文档

## 文件路径
`router/admin_report_router.py`

## 蓝图配置
- **蓝图名称**: `admin_report`
- **URL前缀**: `/api/admin/report`

## 接口列表

### 1. 获取举报列表（管理端）
- **路径**: `/api/admin/report/list`
- **方法**: `GET`
- **函数名**: `get_report_list`
- **OpenAPI摘要**: 获取举报列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| target_type | string | no | 目标类型：post-文章,comment-评论,user-用户 | Query |
| status | string | no | 状态：pending-待处理,handled-已处理,rejected-已驳回 | Query |
| sort | string | no | 排序：created_time，默认created_time | Query |
| order | string | no | 排序方向：asc/desc，默认desc | Query |

#### 请求示例
```
GET /api/admin/report/list?page=1&page_size=20&status=pending&sort=created_time&order=desc&admin_id=1
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "admin_id不能为空"
}
```

> 注：target_title/target_content字段需根据target_type关联posts表（target_type='post'）或comments表（target_type='comment'）查询获取
#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "report_id": 1,
                "reporter": {"user_id": 5, "username": "李四"},
                "target_id": 100,
                "target_type": "post",
                "target_title": "Python入门教程",
                "target_content": "违规文章摘要...",
                "reason": "包含广告信息",
                "status": "pending",
                "handler": null,
                "handle_note": null,
                "created_at": "2024-01-15 10:30:00"
            }
        ],
        "total": 25,
        "page": 1,
        "page_size": 20
    }
}
```

---

### 2. 获取举报详情（管理端）
- **路径**: `/api/admin/report/<report_id>`
- **方法**: `GET`
- **函数名**: `get_report_detail`
- **OpenAPI摘要**: 获取举报详情（含被举报文章完整信息）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| report_id | int | 举报ID |

#### 请求示例
```
GET /api/admin/report/1?admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "report_id": 1,
        "reporter": {"user_id": 5, "username": "李四"},
        "target_id": 100,
        "target_type": "post",
        "target_title": "Python入门教程",
        "target_content": "违规文章摘要...",
        "reason": "包含广告信息",
        "status": "pending",
        "handler": null,
        "handle_note": null,
        "created_at": "2024-01-15 10:30:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "举报不存在"
}
```

---

### 3. 处理举报（管理端）
- **路径**: `/api/admin/report/handle`
- **方法**: `POST`
- **函数名**: `handle_report`
- **OpenAPI摘要**: 处理举报（通过或驳回）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| report_id | int | yes | 举报ID | Body (JSON) |
| action | string | yes | 操作：approve/reject | Body (JSON) |
| handle_note | string | no | 处理备注 | Body (JSON) |
| delete_target | bool | no | 是否删除被举报目标（通过时），默认false | Body (JSON) |
| ban_user | bool | no | 是否封禁被举报用户（通过时），默认false | Body (JSON) |
| ban_duration | int | no | 封禁时长（天），0表示永久，默认7 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "report_id": 1,
    "action": "approve",
    "handle_note": "已确认违规，删除目标内容",
    "delete_target": true,
    "ban_user": false
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "处理成功",
    "data": {
        "report_id": 1,
        "action": "approve",
        "status": "handled",
        "handled_at": "2024-01-15 14:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "举报不存在"
}
```

---

### 4. 批量处理举报（管理端）
- **路径**: `/api/admin/report/batch-handle`
- **方法**: `POST`
- **函数名**: `batch_handle_reports`
- **OpenAPI摘要**: 批量处理多条举报

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 举报ID列表，如[1,2,3] | Body (JSON) |
| action | string | yes | 操作：approve/reject | Body (JSON) |
| handle_note | string | no | 处理备注 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [1, 2, 3],
    "action": "reject",
    "handle_note": "经核实，举报不成立"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "批量处理成功",
    "data": {
        "processed_count": 3,
        "action": "reject"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要处理的举报"
}
```

---

### 5. 处理举报文章（管理端）
- **路径**: `/api/admin/report/article/handle`
- **方法**: `POST`
- **函数名**: `handle_reported_article`
- **OpenAPI摘要**: 处理被举报的文章

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| report_id | int | yes | 举报ID | Body (JSON) |
| action | string | yes | 处理方式：ignore/warn/delete/ban_author | Body (JSON) |
| handle_note | string | no | 处理备注 | Body (JSON) |
| warn_message | string | no | 警告消息（action为warn时） | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "report_id": 1,
    "action": "delete",
    "handle_note": "文章包含违规内容，已删除"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "处理成功",
    "data": {
        "post_id": 100,
        "action": "delete",
        "deleted": true
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 6. 处理举报评论（管理端）
- **路径**: `/api/admin/report/comment/handle`
- **方法**: `POST`
- **函数名**: `handle_reported_comment`
- **OpenAPI摘要**: 处理被举报的评论

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| report_id | int | yes | 举报ID | Body (JSON) |
| action | string | yes | 处理方式：ignore/warn/delete/ban_author | Body (JSON) |
| handle_note | string | no | 处理备注 | Body (JSON) |
| report_ids | array | no | 要处理的举报记录ID列表 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "report_id": 1,
    "action": "delete",
    "handle_note": "评论包含人身攻击，已删除",
    "report_ids": [1, 2]
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "处理成功",
    "data": {
        "comment_id": 50,
        "action": "delete",
        "deleted": true
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "评论不存在"
}
```
