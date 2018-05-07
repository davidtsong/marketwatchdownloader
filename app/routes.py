from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, make_response, send_from_directory, current_app
from app.d import *
from app.genGraphs import *
import os, random, threading, time
import zipfile
# NEED ADD ID HAHAHAHHA / NOW SOMETHING FUNKY ABOUT FILENAMES # ADD WIPER FUNCTION

def downloadData():

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        key = form.username.data
        flash('Login requested for user {}, pass={}'.format(
            form.username.data, form.password.data))
        files = downloadStuffs(form.username.data,form.password.data)
        g = GenGraphs(files, form.username.data)
        filepaths = g.run()
        print(filepaths)
        path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        zipf = zipfile.ZipFile(path+key+'.zip','w', zipfile.ZIP_DEFLATED)
        # zipf.write(app.config['UPLOAD_FOLDER'] + 'stockGraphDataValues.csv')
        # zipf.write(app.config['UPLOAD_FOLDER'] + 'foo.pdf')
        zipf.write(filepaths[0])
        zipf.write(filepaths[1])
        zipf.close()

        return send_from_directory(directory=path, filename=key+'.zip', as_attachment=True)
    return render_template('login.html', title = 'Sign In', form = form)


@app.route('/tests', methods=['GET', 'POST'])
def download():
    path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    key = 'davidsongis@gmail.com'
    filepaths=['app/upload/davidsongis@gmail.com Graphs.pdf','app/upload/davidsongis@gmail.com datapoints.csv']
    zipf = zipfile.ZipFile(path+'f.zip','w', zipfile.ZIP_DEFLATED)
    # zipf.write(app.config['UPLOAD_FOLDER'] + 'stockGraphDataValues.csv')
    # zipf.write(app.config['UPLOAD_FOLDER'] + 'foo.pdf')
    zipf.write(filepaths[0])
    zipf.write(filepaths[1])
    zipf.close()

    return send_from_directory(directory=path, filename='f.zip', as_attachment=True)

    # return send_file('upload/f.zip',
    #         mimetype = 'zip',
    #         attachment_filename= 'f'+'.zip',
    #         as_attachment = True)


#
# def downloadCSV():
#     return send_file(app.config['UPLOAD_FOLDER'] + 'stockGraphDataValues.csv',as_attachment=True, mimetype='text/csv', attachment_filename='stockGraphValues')
#
# @app.route('/downloadPDF')
# def downloadPDF():
#     return send_file(app.config['UPLOAD_FOLDER'] + 'foo.pdf',as_attachment=True, mimetype='application/pdf', attachment_filename='stockGraphValues')
