from flask import Flask, render_template
from extractor import Extractor


app = Flask(__name__)

extractor = Extractor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/learn_front")
def learn_front():
    extract_front, extract_back = extractor.make_card(extractor.pull_random_card())
    return render_template("learn.html", back=extract_back, front=extract_front)


if __name__ == "__main__":
    app.run(debug=True)
