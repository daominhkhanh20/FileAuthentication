from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://b89ca477f65c4c:f458af9c@us-cdbr-east-04.cleardb.com/heroku_835ccb6af698fa5"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://leo:longgiang2010@localhost/video_downloader"
app.config["secret_key"] = "secret_key"

# Initialize the database
db = SQLAlchemy(app)

#Create db model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    hash0 = db.Column(db.LargeBinary(400), nullable=False)
    preview_link = db.Column(db.String(400), nullable=False)
    download_link = db.Column(db.String(400), nullable=False)

    # Create a function to return a string
    def __repr__(self):
        return '<Name %r>' % self.id

#Home page
@app.route('/')
def hello_world():
    db.create_all()
    videos = Video.query.order_by(Video.id)
    return render_template('video_list.html', videos=videos)

#Get javascript files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

#Render preview
@app.route('/video')
def render_video():
    video_name = request.args.get("video_name")
    video = Video.query.filter_by(name=video_name).first()
    return render_template("video_preview.html", video=video)

#Test return binary file
@app.route('/returnfile')
def return_binary():
    video_name = request.args.get("video_name")
    video = Video.query.filter_by(name=video_name).first()
    name = video.download_link
    print(name)
    return video.download_link, video.hash0

if __name__ == "__main__":
    app.run()