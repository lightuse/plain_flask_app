import os
from flask import Flask, flash, make_response, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_assets import Environment, Bundle

from app.model import Subject

UPLOAD_FOLDER = 'app/static/uploads'
IMAGE_FOLDER = 'app/static/images'
MODEL_FOLDER = 'app/static/model'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('stylesheet/stylesheet.scss', filters='pyscss', output='stylesheet/all.css')
assets.register('scss_all', scss)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません', 'failed')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません', 'failed')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # 画像ファイル名にプレフィックスを付ける
            import datetime
            now = datetime.datetime.now()
            pref = '{0:%Y%m%d%H%M%S_}'.format(now)
            filename = pref + secure_filename(file.filename)
            # 保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return render_template("preview.html", filename=filename)

    return render_template("upload.html", filename="")

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route("/select")
def select():
    filename = request.cookies.get('filename', None)
    subject_list = Subject.list()
    return render_template("select.html", filename=filename, subject_list=subject_list)

@app.route("/roulette", methods=['GET', 'POST'])
def roulette():
    if request.method == 'POST':
        subject_index = request.form['subject_index']

        response = make_response(render_template("roulette.html"))
        response.set_cookie('result_index', value=str(subject_index))

        return response

    return render_template("roulette.html")

@app.errorhandler(500)
def system_error(error):
    error_description = error.description
    return render_template("500.html",error_description = error_description)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"),404
