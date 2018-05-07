import os
from flask import Flask, render_template, make_response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guesss'
app.config['UPLOAD_FOLDER'] = "upload/"
from app import routes



if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded = True)
