from flask import Flask, render_template
from extractor import Extractor


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/learn")
def learn():
    extractor = Extractor()
    body_text = extractor.get_definition("demolition")
    return render_template("learn.html", body=body_text)


if __name__ == "__main__":
    app.run(debug=True)
