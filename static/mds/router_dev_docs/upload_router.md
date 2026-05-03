# 文件上传路由接口文档（admin和app共用）

## 文件路径
`router/upload_router.py`

## 蓝图配置
- **蓝图名称**: `upload`
- **URL前缀**: `/api/upload`

## 接口列表

### 1. 文件上传（通用）
- **路径**: `/api/upload/file`
- **方法**: `POST`
- **函数名**: `upload_file`
- **OpenAPI摘要**: 文件上传
- **Content-Type**: `multipart/form-data`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | no | 当前用户ID（不传则按匿名上传处理） | Form Data |
| file | file | yes | 上传的文件（需验证文件大小不超过10MB） | Form Data |

> 注：上传成功后写入files表；user_id未传则files.user_id为NULL
> 注：file_size/file_type/file_path按实际存储生成

#### 请求示例
```
POST /api/upload/file
Content-Type: multipart/form-data

user_id: 1
file: [二进制文件数据]
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 文件信息（上传成功时） |
| data.filename | string | 文件名 |
| data.file_url | string | 文件访问URL |

#### 响应示例（成功）
```json
{
    "code": 200,
    "msg": "上传成功",
    "data": {
        "filename": "example.txt",
        "file_url": "/static/uploads/example.txt"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "未选择文件"
}
```
