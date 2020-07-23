import flask
from flask import Flask, request

app = Flask(__name__)

GITHUB = "https://github.com/hackthemidlands/login_portal"

with open("password.txt") as f:
    PASSWORD = f.read()
with open("flag.txt") as f:
    FLAG = f.read()


@app.route('/')
def index():
    return flask.redirect('home.html')


@app.route('/home.html', methods=["GET", "POST"])
def home():
    success = True
    if request.form.get("username") != "admin":
        success = False
    if request.form.get("password") != PASSWORD:
        success = False

    flag = None
    error = None
    if success:
        flag = FLAG
    if not success and request.method == "POST":
        error = "Invalid username/password details"

    return flask.render_template('home.html', flag=flag, error=error, github=GITHUB)


@app.route('/static/<path:filename>')
def static_files(filename):
    return flask.send_from_directory('files', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
