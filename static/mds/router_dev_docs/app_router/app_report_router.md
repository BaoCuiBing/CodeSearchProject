# 举报路由接口文档

## 文件路径
`router/app_report_router.py`

## 蓝图配置
- **蓝图名称**: `report`
- **URL前缀**: `/api/report`

## 接口列表

### 1. 提交举报（APP端）
- **路径**: `/api/report`
- **方法**: `POST`
- **函数名**: `submit_report`
- **OpenAPI摘要**: 用户提交举报

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| reporter_id | int | yes | 当前用户ID（reports.reporter_id） | Body (JSON) |
| target_id | int | yes | 被举报目标ID | Body (JSON) |
| target_type | string | yes | 目标类型：post-内容,comment-评论,user-用户 | Body (JSON) |
| reason | string | yes | 举报原因（最多500字） | Body (JSON) |

> 注：同一用户对同一目标只能举报一次，重复提交返回400"您已举报过该内容"

#### 请求示例
```json
{
    "reporter_id": 1,
    "target_id": 100,
    "target_type": "post",
    "reason": "该文章包含广告和垃圾信息"
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 举报信息 |
| data.report_id | int | 举报记录ID |

#### 响应示例（成功）
```json
{
    "code": 200,
    "msg": "举报提交成功",
    "data": {
        "report_id": 25
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "举报原因不能为空"
}
```

---

### 2. 获取我的举报列表（APP端）
- **路径**: `/api/report/my-reports`
- **方法**: `GET`
- **函数名**: `get_my_reports`
- **OpenAPI摘要**: 获取当前用户提交的举报记录列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| reporter_id | int | yes | 当前用户ID（reports.reporter_id） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| status | string | no | 状态筛选：pending/handled/rejected/all，默认all | Query |

> 注：target_title字段需根据target_type关联posts表（target_type='post'）或comments表（target_type='comment'）动态查询获取

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 举报列表数据 |
| data.list | array | 举报列表 |
| data.total | int | 总数 |
| data.list[].report_id | int | 举报ID |
| data.list[].target_id | int | 被举报目标ID |
| data.list[].target_type | string | 目标类型 |
| data.list[].target_title | string | 被举报目标标题（动态查询） |
| data.list[].reason | string | 举报原因 |
| data.list[].status | string | 处理状态 |
| data.list[].handle_note | string | 处理备注 |
| data.list[].created_at | datetime | 提交时间 |

#### 请求示例
```
GET /api/report/my-reports?reporter_id=1&page=1&page_size=20&status=all
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "reporter_id不能为空"
}
```
