import time
import os
import random
from flask import Flask, render_template, redirect, url_for, session, jsonify
from flask_dance.contrib.github import make_github_blueprint, github
from threading import Thread
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.secret_key = "your_secret_key"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

github_blueprint = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
)
app.register_blueprint(github_blueprint, url_prefix="/login")

current_number = 0


def number_generator():
    global current_number
    while True:
        current_number = random.randint(1, 100)
        time.sleep(5)


def start_generating_numbers():
    thread = Thread(target=number_generator)
    thread.daemon = True
    thread.start()


@app.route("/")
def index():
    if github.authorized:
        session['authorized'] = True
    else:
        session['authorized'] = False
    return render_template("index.html", authorized=session['authorized'])


@app.route("/logout")
def logout():
    token = github_blueprint.token["access_token"]
    github_blueprint.token = None
    session.clear()
    return redirect(url_for("index"))


@app.route("/number")
def get_number():
    if session.get('authorized'):
        return jsonify({'number': current_number})


if __name__ == "__main__":
    start_generating_numbers()
    app.run(debug=True)
