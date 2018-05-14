import os
from flask import Flask, render_template, make_response
from flask_bootstrap import Bootstrap


def create_app(script_info=None):
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SECRET_KEY'] = 'you-will-never-guesss'
    app.config['UPLOAD_FOLDER'] = "upload/"
    app.config['REDIS_URL'] = "redis://redis:6379/0"
    app.config['QUEUES'] = "default"

    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    app.shell_context_processor({'app':app})

    return app


# if __name__ == '__main__':
#     app.run(debug=True, port=5000, threaded = True)
