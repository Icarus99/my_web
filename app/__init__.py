from flask import Flask, render_template
from app.models.recipe import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    register_blueprint(app)


    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view='web.login'

    db.create_all(app=app)

    return app

def register_blueprint(app):
    from app.web.main import web
    from app.wxapi.main import wxapi
    app.register_blueprint(web)
    app.register_blueprint(wxapi, url_prefix='/wxapi')

def page_not_found(e):
    return render_template('errors/page404.html'), 404

def internal_server_error(e):
    return render_template('errors/page500.html'), 500
