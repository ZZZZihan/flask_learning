from datetime import datetime
from app import db

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(50))  # 论文、专利、项目等
    publish_date = db.Column(db.Date)
    file_url = db.Column(db.String(200))  # 附件链接
    
    # 新增字段
    abstract = db.Column(db.Text)  # 摘要
    keywords = db.Column(db.String(200))  # 关键词
    status = db.Column(db.String(20), default='published')  # 状态：draft, published, archived
    view_count = db.Column(db.Integer, nullable=False, default=0)  # 浏览次数
    
    # 外键关联到用户
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('achievements', lazy='dynamic'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Achievement {self.title}>'
    
    def increment_view(self):
        """增加浏览次数"""
        if self.view_count is None:
            self.view_count = 0
        self.view_count += 1
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
    
    @staticmethod
    def get_categories():
        """获取所有成果类别"""
        return ['论文', '专利', '项目', '获奖', '软件著作权', '其他']
    
    @staticmethod
    def search(query):
        """搜索成果"""
        return Achievement.query.filter(
            (Achievement.title.like(f'%{query}%')) |
            (Achievement.content.like(f'%{query}%')) |
            (Achievement.abstract.like(f'%{query}%')) |
            (Achievement.keywords.like(f'%{query}%'))
        ) 