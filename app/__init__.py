from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
import os
from markupsafe import Markup

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录！'
migrate = Migrate()
bootstrap = Bootstrap()
jwt = JWTManager()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # 创建上传文件夹
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # 添加自定义过滤器
    def nl2br(value):
        return Markup(value.replace('\n', '<br>'))
    
    app.jinja_env.filters['nl2br'] = nl2br
    
    # 注册蓝图
    from app.routes.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.routes.achievement import achievement as achievement_blueprint
    from app.routes.tech_summary import tech_summary as tech_summary_blueprint
    from app.api.v1 import api_v1 as api_v1_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(achievement_blueprint)
    app.register_blueprint(tech_summary_blueprint)
    app.register_blueprint(api_v1_blueprint)
    
    return app 