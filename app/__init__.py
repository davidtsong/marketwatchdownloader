import os
from flask import Flask, render_template, make_response
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'you-will-never-guesss'
app.config['UPLOAD_FOLDER'] = "upload/"
app.config['REDIS_URL'] = "localhost:6379"
from app import routes



if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded = True)
