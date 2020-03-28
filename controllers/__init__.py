import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_crontab import Crontab

from core.config import app_config

toolbar = DebugToolbarExtension()
db = SQLAlchemy()
migrate = Migrate()
crontab = Crontab()


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    app_settings = app_config[os.getenv('APP_SETTINGS', "development")]
    app.config.from_object(app_settings)

    app.config['SECRET_KEY'] = os.getenv("APP_KEY", "o7MQ68S0TOWzURdjTktumKj37NIcI0YN5R0wiKaUd2s=")

    truthy = [0, True, 'true', 'True', 'TRUE']

    app.debug = True if os.getenv("APP_DEBUG") in truthy else False

    db.init_app(app)
    migrate.init_app(app)
    toolbar.init_app(app)
    crontab.init_app(app)

    #########       BLUEPRINTS      ############
    from views.routes import route

    app.register_blueprint(route)

    #########   ERROR HANDLING      #############
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html"), 500

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
