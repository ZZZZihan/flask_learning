from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from app import db
from app.models.achievement import Achievement
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func

achievement = Blueprint('achievement', __name__)

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_achievement_stats():
    """获取成果统计信息"""
    total = Achievement.query.count()
    
    # 获取本月新增数量
    today = datetime.today()
    first_day = datetime(today.year, today.month, 1)
    monthly_count = Achievement.query.filter(Achievement.created_at >= first_day).count()
    
    # 获取总浏览量
    total_views = db.session.query(func.sum(Achievement.view_count)).scalar() or 0
    
    # 获取附件数量
    file_count = Achievement.query.filter(Achievement.file_url.isnot(None)).count()
    
    return {
        'total': total,
        'monthly_count': monthly_count,
        'total_views': total_views,
        'file_count': file_count
    }

@achievement.route('/achievements')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search_query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'newest')  # newest, oldest, views
    
    query = Achievement.query
    
    # 搜索
    if search_query:
        query = Achievement.search(search_query)
    
    # 分类筛选
    if category:
        query = query.filter_by(category=category)
    
    # 排序
    if sort_by == 'newest':
        query = query.order_by(Achievement.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Achievement.created_at.asc())
    elif sort_by == 'views':
        query = query.order_by(Achievement.view_count.desc())
    
    achievements = query.paginate(page=page, per_page=10, error_out=False)
    categories = Achievement.get_categories()
    stats = get_achievement_stats()
    
    return render_template('achievement/index.html',
                         achievements=achievements,
                         categories=categories,
                         current_category=category,
                         search_query=search_query,
                         sort_by=sort_by,
                         monthly_count=stats['monthly_count'],
                         total_views=stats['total_views'],
                         file_count=stats['file_count'])

@achievement.route('/achievements/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        abstract = request.form.get('abstract')
        keywords = request.form.get('keywords')
        publish_date = datetime.strptime(request.form.get('publish_date'), '%Y-%m-%d').date()
        
        achievement = Achievement(
            title=title,
            content=content,
            category=category,
            abstract=abstract,
            keywords=keywords,
            publish_date=publish_date,
            author=current_user
        )
        
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                achievement.file_url = filename
        
        db.session.add(achievement)
        db.session.commit()
        flash('成果添加成功！')
        return redirect(url_for('achievement.index'))
    
    categories = Achievement.get_categories()
    return render_template('achievement/create.html', categories=categories)

@achievement.route('/achievements/<int:id>')
@login_required
def show(id):
    achievement = Achievement.query.get_or_404(id)
    achievement.increment_view()  # 增加浏览次数
    return render_template('achievement/show.html', achievement=achievement)

@achievement.route('/achievements/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    achievement = Achievement.query.get_or_404(id)
    if achievement.author != current_user:
        flash('您没有权限编辑此成果')
        return redirect(url_for('achievement.index'))
    
    if request.method == 'POST':
        achievement.title = request.form.get('title')
        achievement.content = request.form.get('content')
        achievement.category = request.form.get('category')
        achievement.abstract = request.form.get('abstract')
        achievement.keywords = request.form.get('keywords')
        achievement.publish_date = datetime.strptime(request.form.get('publish_date'), '%Y-%m-%d').date()
        
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                # 删除旧文件
                if achievement.file_url:
                    old_file = os.path.join(current_app.config['UPLOAD_FOLDER'], achievement.file_url)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                achievement.file_url = filename
        
        db.session.commit()
        flash('成果更新成功！')
        return redirect(url_for('achievement.show', id=achievement.id))
    
    categories = Achievement.get_categories()
    return render_template('achievement/edit.html', achievement=achievement, categories=categories)

@achievement.route('/achievements/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    achievement = Achievement.query.get_or_404(id)
    if achievement.author != current_user:
        flash('您没有权限删除此成果')
        return redirect(url_for('achievement.index'))
    
    # 删除关联文件
    if achievement.file_url:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], achievement.file_url)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(achievement)
    db.session.commit()
    flash('成果已删除')
    return redirect(url_for('achievement.index'))

@achievement.route('/uploads/<filename>')
@login_required
def download_file(filename):
    """下载文件"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename) 