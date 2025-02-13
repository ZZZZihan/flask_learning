from datetime import datetime
from app import db

class TechSummary(db.Model):
    __tablename__ = 'tech_summaries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(100))  # 标签
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键关联到用户
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('tech_summaries', lazy='dynamic'))
    
    def __repr__(self):
        return f'<TechSummary {self.title}>' 