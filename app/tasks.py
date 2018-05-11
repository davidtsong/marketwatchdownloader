import time
import zipfile
from flask import current_app
from app.d import *
from flask import request, render_template, flash, jsonify, redirect, make_response, send_from_directory, current_app

from app.genGraphs import *

def run(username, password):
    key = username
    files = downloadStuffs(username,password)
    g = GenGraphs(files, username)
    filepaths = g.run()
    print(filepaths)

    path = os.path.join(os.getcwd(), 'app/upload/' + key + '.zip')
    print(os.getcwd() + ' ' + path)

    zipf = zipfile.ZipFile(path,'w', zipfile.ZIP_DEFLATED)
    # zipf.write(app.config['UPLOAD_FOLDER'] + 'stockGraphDataValues.csv')
    # zipf.write(app.config['UPLOAD_FOLDER'] + 'foo.pdf')
    zipf.write(filepaths[0])
    zipf.write(filepaths[1])
    zipf.close()
    return path #return path to download from
    # return send_from_directory(directory=path, filename=key+'.zip', as_attachment=True)
