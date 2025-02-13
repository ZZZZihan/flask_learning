from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.tech_summary import TechSummary
from datetime import datetime

tech_summary = Blueprint('tech_summary', __name__)

@tech_summary.route('/tech_summaries')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    summaries = TechSummary.query.order_by(TechSummary.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('tech_summary/index.html', summaries=summaries)

@tech_summary.route('/tech_summaries/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        
        summary = TechSummary(
            title=title,
            content=content,
            tags=tags,
            author=current_user
        )
        
        db.session.add(summary)
        db.session.commit()
        flash('技术总结添加成功！')
        return redirect(url_for('tech_summary.index'))
    
    return render_template('tech_summary/create.html')

@tech_summary.route('/tech_summaries/<int:id>')
@login_required
def show(id):
    summary = TechSummary.query.get_or_404(id)
    return render_template('tech_summary/show.html', summary=summary)

@tech_summary.route('/tech_summaries/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    summary = TechSummary.query.get_or_404(id)
    if summary.author != current_user:
        flash('您没有权限编辑此技术总结')
        return redirect(url_for('tech_summary.index'))
    
    if request.method == 'POST':
        summary.title = request.form.get('title')
        summary.content = request.form.get('content')
        summary.tags = request.form.get('tags')
        
        db.session.commit()
        flash('技术总结更新成功！')
        return redirect(url_for('tech_summary.show', id=summary.id))
    
    return render_template('tech_summary/edit.html', summary=summary)

@tech_summary.route('/tech_summaries/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    summary = TechSummary.query.get_or_404(id)
    if summary.author != current_user:
        flash('您没有权限删除此技术总结')
        return redirect(url_for('tech_summary.index'))
    
    db.session.delete(summary)
    db.session.commit()
    flash('技术总结已删除')
    return redirect(url_for('tech_summary.index')) 