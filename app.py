from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = "mongodb+srv://test:sparta@cluster0.xqgynan.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/diary", methods=["GET"])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})


@app.route("/diary", methods=["POST"])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename =f'static/post-{mytime}.{extension}'
    file.save(filename)

    profil = request.files['profil_give']
    extension = profil.filename.split('.')[-1]
    profilename =f'static/profil-{mytime}.{extension}'
    profil.save(profilename)
    
    doc = {
        'profil': profilename,
        'file' : filename,
        'title': title_receive, 
        'content': content_receive}
    db.diary.insert_one(doc)
    return jsonify({'msg':'selesai mengupload'})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
