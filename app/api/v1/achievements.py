from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.achievement import Achievement
from app.models.user import User
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

api = Blueprint('api_achievements', __name__)

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', '')
    search_query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'newest')
    
    query = Achievement.query
    
    if search_query:
        query = Achievement.search(search_query)
    
    if category:
        query = query.filter_by(category=category)
    
    if sort_by == 'newest':
        query = query.order_by(Achievement.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Achievement.created_at.asc())
    elif sort_by == 'views':
        query = query.order_by(Achievement.view_count.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    achievements = pagination.items
    
    return jsonify({
        'items': [{
            'id': a.id,
            'title': a.title,
            'content': a.content,
            'abstract': a.abstract,
            'keywords': a.keywords,
            'category': a.category,
            'publish_date': a.publish_date.isoformat() if a.publish_date else None,
            'file_url': a.file_url,
            'view_count': a.view_count,
            'author': {
                'id': a.author.id,
                'username': a.author.username
            },
            'created_at': a.created_at.isoformat(),
            'updated_at': a.updated_at.isoformat()
        } for a in achievements],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@api.route('/achievements/<int:id>', methods=['GET'])
@jwt_required()
def get_achievement(id):
    achievement = Achievement.query.get_or_404(id)
    achievement.increment_view()
    
    return jsonify({
        'id': achievement.id,
        'title': achievement.title,
        'content': achievement.content,
        'abstract': achievement.abstract,
        'keywords': achievement.keywords,
        'category': achievement.category,
        'publish_date': achievement.publish_date.isoformat() if achievement.publish_date else None,
        'file_url': achievement.file_url,
        'view_count': achievement.view_count,
        'author': {
            'id': achievement.author.id,
            'username': achievement.author.username
        },
        'created_at': achievement.created_at.isoformat(),
        'updated_at': achievement.updated_at.isoformat()
    }), 200

@api.route('/achievements', methods=['POST'])
@jwt_required()
def create_achievement():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    data = request.form.to_dict()
    
    achievement = Achievement(
        title=data.get('title'),
        content=data.get('content'),
        abstract=data.get('abstract'),
        keywords=data.get('keywords'),
        category=data.get('category'),
        publish_date=datetime.strptime(data.get('publish_date'), '%Y-%m-%d').date(),
        author=user
    )
    
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            achievement.file_url = filename
    
    db.session.add(achievement)
    db.session.commit()
    
    return jsonify({
        'message': '成果添加成功',
        'id': achievement.id
    }), 201

@api.route('/achievements/<int:id>', methods=['PUT'])
@jwt_required()
def update_achievement(id):
    current_user_id = get_jwt_identity()
    achievement = Achievement.query.get_or_404(id)
    
    if achievement.author_id != current_user_id:
        return jsonify({'message': '您没有权限编辑此成果'}), 403
    
    data = request.form.to_dict()
    
    achievement.title = data.get('title', achievement.title)
    achievement.content = data.get('content', achievement.content)
    achievement.abstract = data.get('abstract', achievement.abstract)
    achievement.keywords = data.get('keywords', achievement.keywords)
    achievement.category = data.get('category', achievement.category)
    if 'publish_date' in data:
        achievement.publish_date = datetime.strptime(data.get('publish_date'), '%Y-%m-%d').date()
    
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
    
    return jsonify({'message': '成果更新成功'}), 200

@api.route('/achievements/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_achievement(id):
    current_user_id = get_jwt_identity()
    achievement = Achievement.query.get_or_404(id)
    
    if achievement.author_id != current_user_id:
        return jsonify({'message': '您没有权限删除此成果'}), 403
    
    if achievement.file_url:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], achievement.file_url)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(achievement)
    db.session.commit()
    
    return jsonify({'message': '成果已删除'}), 200

@api.route('/achievements/categories', methods=['GET'])
@jwt_required()
def get_categories():
    return jsonify({
        'categories': Achievement.get_categories()
    }), 200

@api.route('/achievements/stats', methods=['GET'])
@jwt_required()
def get_stats():
    total = Achievement.query.count()
    
    # 获取本月新增数量
    today = datetime.today()
    first_day = datetime(today.year, today.month, 1)
    monthly_count = Achievement.query.filter(Achievement.created_at >= first_day).count()
    
    # 获取总浏览量
    total_views = db.session.query(db.func.sum(Achievement.view_count)).scalar() or 0
    
    # 获取附件数量
    file_count = Achievement.query.filter(Achievement.file_url.isnot(None)).count()
    
    return jsonify({
        'total': total,
        'monthly_count': monthly_count,
        'total_views': total_views,
        'file_count': file_count
    }), 200 