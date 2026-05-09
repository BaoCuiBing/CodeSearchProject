import os
import re
import json
import shutil
import logging
import markdown2
from config import PROJECT_DIR
from models.db_base import Database, Base
from models.model import User, File, Report, SearchHistory, Category, Post, Tag, PostTag, Comment, Favorite, Like, Follow, Message, Notification, SystemMessage, SystemMessageTarget, SystemSetting
from utils.password_analysis import generate_salt, hash_password

logger = logging.getLogger(__name__)

def _strip_md_tags(text):
    """去除Markdown标识符,只保留纯文本"""
    text = re.sub(r'#{1,6}\s?', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text, flags=re.DOTALL)
    text = re.sub(r'^[-*+]\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def _init_default_data(session):
    """初始化默认数据(管理员账号和系统设置)"""
    logger.info("开始初始化默认数据...")
    admin = session.query(User).filter(User.usernumber == "admin").first()
    if not admin:
        salt = generate_salt()
        hashed_password = hash_password("admin123", salt)
        admin_user = User(usernumber="admin", username="管理员", password=hashed_password, salt=salt, email="wx18455930538@163.com", phone="13800138000", role="admin", avatar="/static/uploads/admin_head.png", bio="我是一名专注于后端开发的工程师，主要从事高性能服务架构设计与系统优化。熟悉 Python 生态及相关框架，具备扎实的网络与系统基础。当前重点关注分布式系统与高并发处理方向，致力于构建稳定、高效的服务系统。", location="上海", website="http://8.130.94.251:5173/", github="https://github.com/BaoCuiBing/CodeSearchKu.git", status="active", is_verified=0)
        session.add(admin_user)
        session.commit()
        logger.info("管理员账号创建完成: usernumber=admin")
    else:
        logger.info("管理员账号已存在,跳过创建")
    settings = [
        {"key": "site_name", "value": "CodeSearch", "description": "站点名称"},
        {"key": "site_description", "value": "CodeSearch是一个专业的代码搜索与知识分享社区，汇聚海量编程教程、技术文档与开源代码资源，支持精准搜索、分类浏览、收藏互动等功能，助力开发者高效学习、快速解决问题，共同成长进步。", "description": "站点描述"},
        {"key": "carousel_imgs", "value": '{"imgs": []}', "description": "首页轮播图"},
        {"key": "special_ancestor_worship", "value": "false", "description": "是否为清明节模式"}
    ]
    for s in settings:
        exist = session.query(SystemSetting).filter(SystemSetting.key == s["key"]).first()
        if not exist:
            setting = SystemSetting(key=s["key"], value=s["value"], description=s["description"])
            session.add(setting)
    session.commit()
    uploads_dir = os.path.join(PROJECT_DIR, "static", "uploads")
    if os.path.exists(uploads_dir):
        admin_avatar_file = os.path.join(PROJECT_DIR, "static", "uploads", "admin_head.png")
        if os.path.exists(admin_avatar_file):
            exist_admin_file = session.query(File).filter(File.filename == "admin_head.png").first()
            if not exist_admin_file:
                admin_file = File(user_id=None, filename="admin_head.png", file_path="uploads/admin_head.png", file_size=0, file_type="image/png", file_url="/static/uploads/admin_head.png")
                session.add(admin_file)
                session.flush()
                admin_avatar_file_id = admin_file.id
            else:
                admin_avatar_file_id = exist_admin_file.id
        for i in range(1, 21):
            filename = f"head_{i}.jpg"
            file_path = os.path.join("uploads", filename)
            file_url = f"/static/uploads/{filename}"
            exist_file = session.query(File).filter(File.filename == filename).first()
            if not exist_file:
                file = File(user_id=None, filename=filename, file_path=file_path, file_size=0, file_type="image/jpeg", file_url=file_url)
                session.add(file)
        session.commit()
    else:
        admin_avatar_file_id = None
    init_lbt_img_dir = os.path.join(PROJECT_DIR, "static", "imgs", "init_lbt_img")
    if os.path.exists(init_lbt_img_dir) and os.path.exists(uploads_dir):
        lbt_images = []
        for img_file in sorted(os.listdir(init_lbt_img_dir)):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                src_path = os.path.join(init_lbt_img_dir, img_file)
                dst_path = os.path.join(uploads_dir, img_file)
                if not os.path.exists(dst_path):
                    shutil.copy2(src_path, dst_path)
                exist_file = session.query(File).filter(File.filename == img_file).first()
                if not exist_file:
                    file_ext = os.path.splitext(img_file)[1].lower()
                    file_type = f"image/{file_ext[1:]}"
                    file_size = os.path.getsize(dst_path) if os.path.exists(dst_path) else 0
                    new_file = File(user_id=None, filename=img_file, file_path=f"uploads/{img_file}", file_size=file_size, file_type=file_type, file_url=f"/static/uploads/{img_file}")
                    session.add(new_file)
                lbt_images.append(f"/static/uploads/{img_file}")
        session.commit()
        carousel_setting = session.query(SystemSetting).filter(SystemSetting.key == "carousel_imgs").first()
        if carousel_setting and lbt_images:
            carousel_setting.value = json.dumps({"imgs": lbt_images})
            session.commit()
    user_data = [
        {"usernumber": "user001", "username": "张三", "email": "zhangsan@example.com", "phone": "13800138001", "bio": "全栈开发工程师", "location": "北京", "website": "https://zhangsan.com", "github": "https://github.com/zhangsan", "avatar": "/static/uploads/head_1.jpg"},
        {"usernumber": "user002", "username": "李四", "email": "lisi@example.com", "phone": "13800138002", "bio": "Python后端开发者", "location": "上海", "website": "https://lisi.com", "github": "https://github.com/lisi", "avatar": "/static/uploads/head_2.jpg"},
        {"usernumber": "user003", "username": "王五", "email": "wangwu@example.com", "phone": "13800138003", "bio": "前端工程师", "location": "广州", "website": "https://wangwu.com", "github": "https://github.com/wangwu", "avatar": "/static/uploads/head_3.jpg"},
        {"usernumber": "user004", "username": "赵六", "email": "zhaoliu@example.com", "phone": "13800138004", "bio": "Java架构师", "location": "深圳", "website": "https://zhaoliu.com", "github": "https://github.com/zhaoliu", "avatar": "/static/uploads/head_4.jpg"},
        {"usernumber": "user005", "username": "孙七", "email": "sunqi@example.com", "phone": "13800138005", "bio": "数据工程师", "location": "杭州", "website": "https://sunqi.com", "github": "https://github.com/sunqi", "avatar": "/static/uploads/head_5.jpg"},
        {"usernumber": "user006", "username": "周八", "email": "zhouba@example.com", "phone": "13800138006", "bio": "DevOps工程师", "location": "成都", "website": "https://zhouba.com", "github": "https://github.com/zhouba", "avatar": "/static/uploads/head_6.jpg"},
        {"usernumber": "user007", "username": "吴九", "email": "wujiu@example.com", "phone": "13800138007", "bio": "AI研究员", "location": "武汉", "website": "https://wujiu.com", "github": "https://github.com/wujiu", "avatar": "/static/uploads/head_7.jpg"},
        {"usernumber": "user008", "username": "郑十", "email": "zhengshi@example.com", "phone": "13800138008", "bio": "安全工程师", "location": "西安", "website": "https://zhengshi.com", "github": "https://github.com/zhengshi", "avatar": "/static/uploads/head_8.jpg"},
        {"usernumber": "user009", "username": "钱一", "email": "qianyi@example.com", "phone": "13800138009", "bio": "产品经理", "location": "南京", "website": "https://qianyi.com", "github": "https://github.com/qianyi", "avatar": "/static/uploads/head_9.jpg"},
        {"usernumber": "user010", "username": "陈二", "email": "chener@example.com", "phone": "13800138010", "bio": "测试工程师", "location": "重庆", "website": "https://chener.com", "github": "https://github.com/chener", "avatar": "/static/uploads/head_10.jpg"},
        {"usernumber": "user011", "username": "刘三", "email": "liusan@example.com", "phone": "13800138011", "bio": "运维工程师", "location": "天津", "website": "https://liusan.com", "github": "https://github.com/liusan", "avatar": "/static/uploads/head_11.jpg"},
        {"usernumber": "user012", "username": "黄四", "email": "huangsi@example.com", "phone": "13800138012", "bio": "架构师", "location": "苏州", "website": "https://huangsi.com", "github": "https://github.com/huangsi", "avatar": "/static/uploads/head_12.jpg"},
        {"usernumber": "user013", "username": "杨五", "email": "yangwu@example.com", "phone": "13800138013", "bio": "移动端开发者", "location": "长沙", "website": "https://yangwu.com", "github": "https://github.com/yangwu", "avatar": "/static/uploads/head_13.jpg"},
        {"usernumber": "user014", "username": "林六", "email": "linliu@example.com", "phone": "13800138014", "bio": "游戏开发者", "location": "昆明", "website": "https://linliu.com", "github": "https://github.com/linliu", "avatar": "/static/uploads/head_14.jpg"},
        {"usernumber": "user015", "username": "徐七", "email": "xuqi@example.com", "phone": "13800138015", "bio": "数据库管理员", "location": "沈阳", "website": "https://xuqi.com", "github": "https://github.com/xuqi", "avatar": "/static/uploads/head_15.jpg"},
        {"usernumber": "user016", "username": "许八", "email": "xuba@example.com", "phone": "13800138016", "bio": "云计算工程师", "location": "济南", "website": "https://xuba.com", "github": "https://github.com/xuba", "avatar": "/static/uploads/head_16.jpg"},
        {"usernumber": "user017", "username": "何九", "email": "hejiu@example.com", "phone": "13800138017", "bio": "区块链开发者", "location": "大连", "website": "https://hejiu.com", "github": "https://github.com/hejiu", "avatar": "/static/uploads/head_17.jpg"},
        {"usernumber": "user018", "username": "高十", "email": "gaoshi@example.com", "phone": "13800138018", "bio": "网络工程师", "location": "青岛", "website": "https://gaoshi.com", "github": "https://github.com/gaoshi", "avatar": "/static/uploads/head_18.jpg"},
        {"usernumber": "user019", "username": "马一", "email": "mayi@example.com", "phone": "13800138019", "bio": "嵌入式开发者", "location": "福州", "website": "https://mayi.com", "github": "https://github.com/mayi", "avatar": "/static/uploads/head_19.jpg"},
        {"usernumber": "user020", "username": "朱二", "email": "zhuer@example.com", "phone": "13800138020", "bio": "技术作家", "location": "厦门", "website": "https://zhuer.com", "github": "https://github.com/zhuer", "avatar": "/static/uploads/head_20.jpg"}
    ]
    for ud in user_data:
        exist_user = session.query(User).filter(User.usernumber == ud["usernumber"]).first()
        if not exist_user:
            salt = generate_salt()
            hashed_password = hash_password("user123", salt)
            user = User(usernumber=ud["usernumber"], username=ud["username"], password=hashed_password, salt=salt, email=ud["email"], phone=ud["phone"], role="user", avatar=ud["avatar"], bio=ud["bio"], location=ud["location"], website=ud["website"], github=ud["github"], status="active", is_verified=0)
            session.add(user)
    session.commit()
    tag_data = [
        {"name": "Python", "slug": "python", "description": "Python编程语言", "color": "#1989fa", "is_hot": 1, "is_recommend": 1},
        {"name": "JavaScript", "slug": "javascript", "description": "JavaScript前端开发", "color": "#ff6b6b", "is_hot": 1, "is_recommend": 1},
        {"name": "Vue", "slug": "vue", "description": "Vue前端框架", "color": "#42b883", "is_hot": 1, "is_recommend": 1},
        {"name": "React", "slug": "react", "description": "React前端框架", "color": "#61dafb", "is_hot": 1, "is_recommend": 1},
        {"name": "Docker", "slug": "docker", "description": "容器化部署", "color": "#2496ed", "is_hot": 1, "is_recommend": 1},
        {"name": "MySQL", "slug": "mysql", "description": "MySQL数据库", "color": "#4479a1", "is_hot": 1, "is_recommend": 1},
        {"name": "Redis", "slug": "redis", "description": "Redis缓存数据库", "color": "#dc382d", "is_hot": 1, "is_recommend": 0},
        {"name": "Linux", "slug": "linux", "description": "Linux系统运维", "color": "#fcc624", "is_hot": 1, "is_recommend": 1},
        {"name": "Go", "slug": "go", "description": "Go语言后端开发", "color": "#00add8", "is_hot": 1, "is_recommend": 0},
        {"name": "Java", "slug": "java", "description": "Java企业级开发", "color": "#007396", "is_hot": 1, "is_recommend": 1},
        {"name": "并发", "slug": "concurrency", "description": "多线程并发编程", "color": "#7232dd", "is_hot": 0, "is_recommend": 0},
        {"name": "前端", "slug": "frontend", "description": "前端开发技术", "color": "#8e44ad", "is_hot": 0, "is_recommend": 0},
        {"name": "数据库", "slug": "database", "description": "数据库技术", "color": "#2ecc71", "is_hot": 0, "is_recommend": 0},
        {"name": "运维", "slug": "devops", "description": "运维部署相关", "color": "#e67e22", "is_hot": 0, "is_recommend": 0},
        {"name": "算法", "slug": "algorithm", "description": "算法与数据结构", "color": "#3498db", "is_hot": 0, "is_recommend": 1},
        {"name": "数据结构", "slug": "data-structure", "description": "数据结构设计", "color": "#9b59b6", "is_hot": 0, "is_recommend": 0},
        {"name": "Git", "slug": "git", "description": "版本控制系统", "color": "#f05032", "is_hot": 0, "is_recommend": 0},
        {"name": "网络安全", "slug": "security", "description": "网络安全技术", "color": "#e74c3c", "is_hot": 0, "is_recommend": 0},
        {"name": "云计算", "slug": "cloud", "description": "云计算与分布式", "color": "#00bcd4", "is_hot": 0, "is_recommend": 1},
        {"name": "UI设计", "slug": "ui-design", "description": "界面设计与交互", "color": "#ff4081", "is_hot": 0, "is_recommend": 0}
    ]
    for idx, td in enumerate(tag_data):
        exist_tag = session.query(Tag).filter(Tag.name == td["name"]).first()
        if not exist_tag:
            tag = Tag(name=td["name"], slug=td["slug"], description=td["description"], color=td["color"], post_count=0, is_hot=td["is_hot"], is_recommend=td["is_recommend"], sort_order=idx, status="active")
            session.add(tag)
    session.commit()
    pots_mds_dir = os.path.join(PROJECT_DIR, "static", "mds", "pots_mds")
    if os.path.exists(pots_mds_dir):
        admin_user = session.query(User).filter(User.usernumber == "admin").first()
        sort_idx = 0
        folder_list = sorted(os.listdir(pots_mds_dir))
        total_folders = len([f for f in folder_list if os.path.isdir(os.path.join(pots_mds_dir, f))])
        logger.info(f"开始导入教程数据: 共{total_folders}个分类目录")
        for folder_name in folder_list:
            folder_path = os.path.join(pots_mds_dir, folder_name)
            if os.path.isdir(folder_path):
                exist_cat = session.query(Category).filter(Category.name == folder_name).first()
                if not exist_cat:
                    category = Category(name=folder_name, description=f"{folder_name}教程分类", sort=sort_idx)
                    session.add(category)
                    session.flush()
                    sort_idx += 1
                    cat_id = category.id
                    logger.debug(f"创建分类: {folder_name}")
                else:
                    cat_id = exist_cat.id
                    logger.debug(f"分类已存在: {folder_name}")
                html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
                for html_file in html_files:
                    html_path = os.path.join(folder_path, html_file)
                    with open(html_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    title = os.path.splitext(html_file)[0]
                    exist_post = session.query(Post).filter(Post.title == title, Post.category_id == cat_id).first()
                    if not exist_post:
                        plain_text = re.sub(r'<[^>]+>', '', content)
                        plain_text = re.sub(r'\s{2,}', ' ', plain_text).strip()
                        plain_text = re.sub(r'https?://\S+', '', plain_text)
                        summary = plain_text[:200] if len(plain_text) > 200 else plain_text
                        post = Post(user_id=admin_user.id, category_id=cat_id, title=title, content=content, summary=summary, cover_image='{"imgs": []}', type="article", status="published")
                        session.add(post)
                logger.info(f"分类[{folder_name}]导入完成: {len(html_files)}篇文章")
        session.commit()
        logger.info(f"教程数据导入完成: 共{total_folders}个分类")
    init_tag_img_dir = os.path.join(PROJECT_DIR, "static", "imgs", "init_tag_img")
    tag_icon_map_path = os.path.join(init_tag_img_dir, "tag_icon_map.json")
    if os.path.exists(init_tag_img_dir) and os.path.exists(tag_icon_map_path) and os.path.exists(uploads_dir):
        with open(tag_icon_map_path, "r", encoding="utf-8") as f:
            tag_icon_map = json.load(f)
        logger.info(f"开始导入分类图标: 共{len(tag_icon_map)}个")
        icon_url_map = {}
        for folder_name, img_file in tag_icon_map.items():
            src_path = os.path.join(init_tag_img_dir, img_file)
            if not os.path.exists(src_path):
                logger.warning(f"图标文件不存在: {img_file}")
                continue
            dst_path = os.path.join(uploads_dir, img_file)
            if not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)
            exist_file = session.query(File).filter(File.filename == img_file).first()
            if not exist_file:
                file_ext = os.path.splitext(img_file)[1].lower()
                file_type = f"image/{file_ext[1:]}"
                file_size = os.path.getsize(dst_path) if os.path.exists(dst_path) else 0
                new_file = File(user_id=None, filename=img_file, file_path=f"uploads/{img_file}", file_size=file_size, file_type=file_type, file_url=f"/static/uploads/{img_file}")
                session.add(new_file)
                session.flush()
                icon_url_map[folder_name] = f"/static/uploads/{img_file}"
            else:
                icon_url_map[folder_name] = exist_file.file_url
        session.commit()
        for cat in session.query(Category).all():
            if cat.name in icon_url_map:
                cat.icon = icon_url_map[cat.name]
        session.commit()
        logger.info(f"分类图标导入完成: 共{len(icon_url_map)}个")
    logger.info("开始关联标签与文章...")
    tag_map = {tag.name: tag for tag in session.query(Tag).all()}
    cat_map = {cat.id: cat.name for cat in session.query(Category).all()}
    existing_pt = set((pt.post_id, pt.tag_id) for pt in session.query(PostTag).all())
    all_posts = session.query(Post).all()
    tag_category_map = {
        "Python": ["Python"],
        "JavaScript": ["JavaScript", "JS", "AJAX"],
        "Vue": ["Vue"],
        "React": ["React"],
        "Docker": ["Docker"],
        "MySQL": ["MySQL", "SQL"],
        "Redis": ["Redis"],
        "Linux": ["Linux"],
        "Go": ["Go"],
        "Java": ["Java"],
        "前端": ["HTML", "CSS", "JavaScript", "Vue", "React", "Bootstrap", "Angular", "jQuery", "前端", "AppML", "SVG", "Canvas", "Sass", "Less", "Tailwind", "Echarts", "Chart.js", "Highcharts", "D3.js"],
        "数据库": ["MySQL", "SQL", "Redis", "MongoDB", "SQLite", "数据库"],
        "运维": ["Docker", "Linux", "Nginx", "Apache", "运维", "部署", "服务器", "Zookeeper"],
        "算法": ["算法", "数据结构"],
        "数据结构": ["数据结构"],
        "Git": ["Git", "SVN", "版本控制"],
        "网络安全": ["安全", "网络", "协议", "TCP"],
        "云计算": ["云", "AWS", "Azure", "Docker", "Kubernetes"],
        "UI设计": ["UI", "设计", "CSS", "Bootstrap", "Tailwind"],
    }
    post_tag_count = 0
    for post in all_posts:
        cat_name = cat_map.get(post.category_id, "")
        if not cat_name:
            continue
        for tag_name, keywords in tag_category_map.items():
            if tag_name not in tag_map:
                continue
            if any(kw.lower() in cat_name.lower() for kw in keywords):
                tag_id = tag_map[tag_name].id
                if (post.id, tag_id) not in existing_pt:
                    session.add(PostTag(post_id=post.id, tag_id=tag_id))
                    existing_pt.add((post.id, tag_id))
                    post_tag_count += 1
    session.commit()
    logger.info(f"标签关联完成: 共{post_tag_count}条关联")
    for tag in session.query(Tag).all():
        count = session.query(PostTag).filter(PostTag.tag_id == tag.id).count()
        tag.post_count = count
    session.commit()
    logger.info("标签文章计数更新完成")
    user_map = {u.username: u.id for u in session.query(User).all()}
    post_ids = [p.id for p in session.query(Post.id).order_by(Post.id).all()]
    comment_data = [
        {"user_id": user_map["张三"], "post_id": post_ids[0], "content": "这篇文章写得非常好，对我学习OpenCode很有帮助！"},
        {"user_id": user_map["李四"], "post_id": post_ids[0], "content": "请问有没有更详细的部署教程？"},
        {"user_id": user_map["王五"], "post_id": post_ids[1], "content": "AI Agent的开发思路很清晰，受益匪浅"},
        {"user_id": user_map["赵六"], "post_id": post_ids[2], "content": "生产部署这部分内容非常实用，收藏了"},
        {"user_id": user_map["孙七"], "post_id": post_ids[3], "content": "安全性评估是AI应用的重要环节，讲得很透彻"}
    ]
    for cd in comment_data:
        exist = session.query(Comment).filter(Comment.user_id == cd["user_id"], Comment.post_id == cd["post_id"], Comment.content == cd["content"]).first()
        if not exist:
            session.add(Comment(user_id=cd["user_id"], post_id=cd["post_id"], content=cd["content"]))
    session.commit()
    favorite_data = [
        {"user_id": user_map["张三"], "post_id": post_ids[0]},
        {"user_id": user_map["李四"], "post_id": post_ids[0]},
        {"user_id": user_map["王五"], "post_id": post_ids[1]},
        {"user_id": user_map["赵六"], "post_id": post_ids[2]},
        {"user_id": user_map["孙七"], "post_id": post_ids[3]}
    ]
    for fd in favorite_data:
        exist = session.query(Favorite).filter(Favorite.user_id == fd["user_id"], Favorite.post_id == fd["post_id"]).first()
        if not exist:
            session.add(Favorite(user_id=fd["user_id"], post_id=fd["post_id"]))
    session.commit()
    like_data = [
        {"user_id": user_map["张三"], "target_id": post_ids[0], "target_type": "post"},
        {"user_id": user_map["李四"], "target_id": post_ids[0], "target_type": "post"},
        {"user_id": user_map["王五"], "target_id": post_ids[1], "target_type": "post"},
        {"user_id": user_map["赵六"], "target_id": post_ids[2], "target_type": "post"},
        {"user_id": user_map["孙七"], "target_id": post_ids[3], "target_type": "post"}
    ]
    for ld in like_data:
        exist = session.query(Like).filter(Like.user_id == ld["user_id"], Like.target_id == ld["target_id"], Like.target_type == ld["target_type"]).first()
        if not exist:
            session.add(Like(user_id=ld["user_id"], target_id=ld["target_id"], target_type=ld["target_type"]))
    session.commit()
    follow_data = [
        {"follower_id": user_map["张三"], "following_id": admin_user.id},
        {"follower_id": user_map["李四"], "following_id": admin_user.id},
        {"follower_id": user_map["王五"], "following_id": user_map["张三"]},
        {"follower_id": user_map["赵六"], "following_id": user_map["李四"]},
        {"follower_id": user_map["孙七"], "following_id": user_map["王五"]}
    ]
    for fd in follow_data:
        exist = session.query(Follow).filter(Follow.follower_id == fd["follower_id"], Follow.following_id == fd["following_id"]).first()
        if not exist:
            session.add(Follow(follower_id=fd["follower_id"], following_id=fd["following_id"]))
    session.commit()
    report_data = [
        {"reporter_id": user_map["张三"], "target_id": post_ids[4], "target_type": "post", "reason": "内容包含不实信息，误导读者"},
        {"reporter_id": user_map["李四"], "target_id": 2, "target_type": "comment", "reason": "评论内容含有广告推广信息"},
        {"reporter_id": user_map["王五"], "target_id": 6, "target_type": "user", "reason": "该用户发布大量垃圾信息"}
    ]
    for rd in report_data:
        exist = session.query(Report).filter(Report.reporter_id == rd["reporter_id"], Report.target_id == rd["target_id"], Report.target_type == rd["target_type"]).first()
        if not exist:
            session.add(Report(reporter_id=rd["reporter_id"], target_id=rd["target_id"], target_type=rd["target_type"], reason=rd["reason"]))
    session.commit()
    message_data = [
        {"from_user_id": user_map["张三"], "to_user_id": user_map["李四"], "content": "李四你好，看到你也收藏了OpenCode入门教程，一起交流学习吧！", "is_read": 1},
        {"from_user_id": user_map["李四"], "to_user_id": user_map["张三"], "content": "好的张三！我最近也在研究这个，有什么问题可以互相讨论", "is_read": 0},
        {"from_user_id": user_map["王五"], "to_user_id": user_map["赵六"], "content": "赵六，你写的生产部署文章太实用了，想请教一下Docker部署的问题", "is_read": 1},
        {"from_user_id": user_map["赵六"], "to_user_id": user_map["王五"], "content": "没问题，Docker部署这块我比较熟，随时可以交流", "is_read": 1},
        {"from_user_id": user_map["孙七"], "to_user_id": admin_user.id, "content": "管理员您好，我想申请成为社区认证作者，请问需要什么条件？", "is_read": 0}
    ]
    for md in message_data:
        exist = session.query(Message).filter(Message.from_user_id == md["from_user_id"], Message.to_user_id == md["to_user_id"], Message.content == md["content"]).first()
        if not exist:
            session.add(Message(from_user_id=md["from_user_id"], to_user_id=md["to_user_id"], content=md["content"], is_read=md["is_read"]))
    session.commit()
    search_history_data = [
        {"user_id": user_map["张三"], "keyword": "Python异步编程"},
        {"user_id": user_map["张三"], "keyword": "FastAPI教程"},
        {"user_id": user_map["李四"], "keyword": "Vue3组合式API"},
        {"user_id": user_map["李四"], "keyword": "Docker部署"},
        {"user_id": user_map["王五"], "keyword": "React Hooks"},
        {"user_id": user_map["王五"], "keyword": "TypeScript入门"},
        {"user_id": user_map["赵六"], "keyword": "MySQL优化"},
        {"user_id": user_map["赵六"], "keyword": "Redis缓存策略"},
        {"user_id": user_map["孙七"], "keyword": "Linux常用命令"},
        {"user_id": user_map["孙七"], "keyword": "Git版本控制"}
    ]
    for sd in search_history_data:
        session.add(SearchHistory(user_id=sd["user_id"], keyword=sd["keyword"]))
    session.commit()
    admin_sender = session.query(User).filter(User.usernumber == "admin").first()
    exist_msg = session.query(SystemMessage).filter(SystemMessage.title == "欢迎使用本软件").first()
    if not exist_msg and admin_sender:
        content = "尊敬的用户，您好！衷心感谢您选择使用代码搜索社区Pro。我们团队倾力打造这款软件，致力于为您提供高效、便捷、智能的代码搜索与知识分享平台。在这里，您可以快速搜索海量技术文档与开源代码，浏览精心整理的编程教程，收藏有价值的技术文章，还能与广大开发者互动交流、共同成长。我们持续优化搜索引擎算法，不断丰富内容资源库，力求每一次更新都能为您带来更流畅、更精准的使用体验。无论您是初学者还是资深工程师，都能在这里找到所需的知识与灵感。如果您在使用过程中有任何建议或遇到任何问题，欢迎随时通过站内信或GitHub Issues向我们反馈。您的每一条意见都是我们改进的方向，您的支持与信任是我们不断前进的最大动力。祝您使用愉快，编码顺利，技术精进！"
        msg = SystemMessage(sender_id=admin_sender.id, title="欢迎使用本软件", content=content, type="announcement", target_type="all", priority="high", is_top=1, status="sent")
        session.add(msg)
        session.flush()
        all_users = session.query(User).all()
        for u in all_users:
            session.add(SystemMessageTarget(message_id=msg.id, user_id=u.id))
        session.commit()

def init_database():
    """初始化数据库,创建表结构"""
    logger.info("开始初始化数据库...")
    db = Database()
    db.create_tables()
    logger.info("数据库表创建完成")
    session = db.get_session()
    try:
        _init_default_data(session)
        logger.info("数据库初始化完成")
    finally:
        session.close()
    return db

def reset_database():
    """重置数据库,删除所有表后重新创建"""
    db = Database()
    session = db.get_session()
    try:
        print("正在删除所有数据表...")
        Base.metadata.drop_all(bind=db.engine)
        print("数据表删除完成")
        print("正在创建数据表...")
        Base.metadata.create_all(bind=db.engine)
        print("数据表创建完成")
        _init_default_data(session)
        print("管理员账号创建完成: usernumber=admin, password=admin123")
        print("系统设置初始化完成")
    finally:
        session.close()
    return db

def get_db_session(db: Database):
    """获取数据库会话生成器,用于依赖注入"""
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

if __name__ == "__main__":
    reset_database()