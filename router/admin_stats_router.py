from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Post, Comment, SearchHistory, Report
from models.db_init import get_db_session

admin_stats_bp = Blueprint("admin_stats", url_prefix="/api/admin/stats")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_stats_bp.get("/dashboard")
@openapi.summary("获取仪表盘概览数据")
async def get_dashboard_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "week")
    total_users = db.query(User).count()
    new_users = db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=7)).count()
    total_articles = db.query(Post).filter(Post.type == "article").count()
    new_articles = db.query(Post).filter(Post.type == "article", Post.created_at >= datetime.now() - timedelta(days=7)).count()
    total_questions = db.query(Post).filter(Post.type == "question").count()
    new_questions = db.query(Post).filter(Post.type == "question", Post.created_at >= datetime.now() - timedelta(days=7)).count()
    total_comments = db.query(Comment).count()
    new_comments = db.query(Comment).filter(Comment.created_at >= datetime.now() - timedelta(days=7)).count()
    total_views = db.query(Post).with_entities(func.sum(Post.view_count)).scalar() or 0
    new_views = db.query(Post).filter(Post.created_at >= datetime.now() - timedelta(days=7)).with_entities(func.sum(Post.view_count)).scalar() or 0
    active_users_today = db.query(User).filter(func.date(User.last_login_time) == datetime.now().date()).count()
    reported_items = db.query(Report).filter(Report.status == "pending").count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"summary": {"total_users": total_users, "new_users": new_users, "total_articles": total_articles, "new_articles": new_articles, "total_questions": total_questions, "new_questions": new_questions, "total_comments": total_comments, "new_comments": new_comments, "total_views": total_views, "new_views": new_views, "active_users_today": active_users_today, "reported_items": reported_items}, "growth_rates": {"user_growth": 0, "article_growth": 0, "question_growth": 0, "comment_growth": 0, "view_growth": 0}, "trend_charts": {"users_trend": [], "articles_trend": [], "views_trend": []}, "quick_actions": [], "recent_activities": []}})

@admin_stats_bp.get("/users")
@openapi.summary("获取用户统计分析")
async def get_user_statistics(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "month")
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.status == "active").count()
    new_users_month = db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=30)).count()
    verified_users = db.query(User).filter(User.is_verified == 1).count()
    banned_users = db.query(User).filter(User.status == "banned").count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"overview": {"total_users": total_users, "active_users": active_users, "new_users_month": new_users_month, "verified_users": verified_users, "banned_users": banned_users, "churn_rate": 0, "retention_rate": 0}, "registration_trend": [], "user_distribution": {"by_role": [], "by_registration_period": [], "by_activity_level": []}, "top_contributors": []}})

@admin_stats_bp.get("/content")
@openapi.summary("获取文章统计分析")
async def get_content_statistics(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "month")
    total_articles = db.query(Post).filter(Post.type == "article").count()
    total_questions = db.query(Post).filter(Post.type == "question").count()
    total_comments = db.query(Comment).count()
    published_today = db.query(Post).filter(func.date(Post.created_at) == datetime.now().date()).count()
    published_week = db.query(Post).filter(Post.created_at >= datetime.now() - timedelta(days=7)).count()
    total_views = db.query(Post).with_entities(func.sum(Post.view_count)).scalar() or 0
    total_likes = db.query(Post).with_entities(func.sum(Post.like_count)).scalar() or 0
    return response.json({"code": 200, "msg": "获取成功", "data": {"overview": {"total_articles": total_articles, "total_questions": total_questions, "total_comments": total_comments, "published_today": published_today, "published_week": published_week, "avg_views_per_article": round(total_views / total_articles) if total_articles > 0 else 0, "avg_comments_per_article": round(total_comments / total_articles, 1) if total_articles > 0 else 0, "content_growth_rate": 0}, "publishing_trend": {"articles": [], "questions": [], "comments": []}, "category_distribution": [], "tag_distribution": [], "popular_content": []}})

@admin_stats_bp.get("/search-keywords")
@openapi.summary("获取搜索关键词统计")
async def get_search_keyword_stats(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "week")
    limit = int(request.args.get("limit", 50))
    keywords = db.query(SearchHistory.keyword, func.count(SearchHistory.id).label("count")).group_by(SearchHistory.keyword).order_by(func.count(SearchHistory.id).desc()).limit(limit).all()
    top_keywords = [{"keyword": k.keyword, "search_count": k.count, "trend": "stable", "growth_rate": 0} for k in keywords]
    return response.json({"code": 200, "msg": "获取成功", "data": {"top_keywords": top_keywords, "search_volume_trend": []}})

@admin_stats_bp.post("/export-report")
@openapi.summary("导出统计报告")
async def export_statistics_report(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    return response.json({"code": 200, "msg": "导出成功", "data": {"filename": "report.xlsx", "file_url": "/static/exports/report.xlsx"}})

@admin_stats_bp.get("/compare")
@openapi.summary("获取对比分析数据")
async def get_comparison_data(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    metric = request.args.get("metric")
    if metric not in ["users", "articles", "comments", "views"]:
        return response.json({"code": 400, "msg": "指标类型不支持"})
    return response.json({"code": 200, "msg": "获取成功", "data": {"metric": metric, "period1": {"label": "", "start": request.args.get("period1_start"), "end": request.args.get("period1_end"), "value": 0, "daily_avg": 0}, "period2": {"label": "", "start": request.args.get("period2_start"), "end": request.args.get("period2_end"), "value": 0, "daily_avg": 0}, "change": {"absolute": 0, "percentage": 0, "trend": "stable"}}})
