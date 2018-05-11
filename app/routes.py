from app import app
from app.forms import LoginForm
from flask import Response, request, render_template, flash, url_for, jsonify, redirect, make_response, send_file, current_app
import os, random, threading, time
import redis
from app import tasks
from flask import Blueprint, render_template, request, jsonify, current_app, g
from rq import push_connection, pop_connection, Queue

# NEED ADD ID HAHAHAHHA / NOW SOMETHING FUNKY ABOUT FILENAMES # ADD WIPER FUNCTION

def get_redis_connection():
    redis_connection = getattr(g, '_redis_connection', None)
    if redis_connection is None:
        redis_url = current_app.config['REDIS_URL']
        redis_connection = g._redis_connection = redis.from_url(redis_url)
    return redis_connection

@app.before_request
def push_rq_connection():
    push_connection(get_redis_connection())


@app.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()

@app.route('/status/<job_id>')
def job_status(job_id):
    q = Queue()
    job = q.fetch_job(job_id)
    if job is None:
        response = {'status': 'unknown'}
    else:
        response = {
            'status': job.get_status(),
            'result': job.result,
        }
        if job.is_failed:
            response['message'] = job.exc_info.strip().split('\n')[-1]
    return jsonify(response)

@app.route('/download/<job_id>')
def job_download(job_id):
    q = Queue()
    job = q.fetch_job(job_id)
    file = job.result
    if job is None:
        flash('Failed', 'danger')
    else:
    #    return Response(os.open(job.result).read(), mimetype="application/zip", headers={'Content-Disposition':'attachment;filename=stockproject.zip'})
         return send_file(job.result, attachment_filename='Your Stock Project.zip')

@app.route('/_runProgram', methods = ['POST'])
def runProgram():
    username = request.form.get('username')
    password = request.form.get('password')
    #print("req for " + username + " " + password)
    #flash('Req for: {} w/ pass {}'.format(username,password), 'success')
    q = Queue()
    job = q.enqueue(tasks.run, username, password)
    print(url_for('job_status', job_id=job.get_id()))
    return jsonify({}), 202, {'Location': url_for('job_status', job_id=job.get_id()), 'id': job.get_id()}

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    # if form.validate_on_submit():
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     try:
    #         result = 'Yellow'
    #     except Exception as e:
    #         flash('Task failed: {}'.format(e), 'danger')
    #     else:
    #         flash(result, 'success')
    #     return redirect(url_for('index.html'))
    return render_template('login.html', form = form)
    # if form.validate_on_submit():
    #     key = form.username.data
    #     flash('Login requested for user {}, pass={}'.format(
    #         form.username.data, form.password.data))
    #     files = downloadStuffs(form.username.data,form.password.data)
    #     g = GenGraphs(files, form.username.data)
    #     filepaths = g.run()
    #     print(filepaths)
    #     path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    #     zipf = zipfile.ZipFile(path+key+'.zip','w', zipfile.ZIP_DEFLATED)
    #     # zipf.write(app.config['UPLOAD_FOLDER'] + 'stockGraphDataValues.csv')
    #     # zipf.write(app.config['UPLOAD_FOLDER'] + 'foo.pdf')
    #     zipf.write(filepaths[0])
    #     zipf.write(filepaths[1])
    #     zipf.close()
    #
    #     return send_from_directory(directory=path, filename=key+'.zip', as_attachment=True)
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
