from color_manager import ColorManager
from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from base64 import b64encode


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///img.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return redirect(url_for('analyse_colors', pic_id=img.id))


@app.route('/colors/<int:pic_id>')
def analyse_colors(pic_id):
    img = Img.query.filter_by(id=pic_id).first()
    img_converted = b64encode(img.img).decode("utf-8")
    if not img:
        return 'Img Not Found!', 404
    chart_mgr = ColorManager()
    colors = chart_mgr.get_colors(img.img, 8)
    return render_template('colors.html', colors=colors, image=img_converted)


if __name__ == "__main__":
    app.run(debug=True)
