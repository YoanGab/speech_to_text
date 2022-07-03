from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    Bootstrap(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
