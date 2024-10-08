from flask import Flask, render_template, redirect, url_for, request
from extractor import Extractor


app = Flask(__name__)

extractor = Extractor()


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/learn_front")
def learn_front():
    w_title, w_phonetics, w_definition, w_example = extractor.make_card(extractor.pull_random_card())
    return render_template("learn.html", title=w_title, phonetics=w_phonetics,
                           definition=w_definition, example=w_example)


@app.route("/easy_scale", methods=["POST"])
def easy_scale():
    title = request.form.get("w_title")
    extractor.easy_scale(title)
    return redirect(url_for("learn_front"))


@app.route("/medium_scale", methods=["POST"])
def medium_scale():
    title = request.form.get("w_title")
    extractor.medium_scale(title)
    return redirect(url_for("learn_front"))


@app.route("/hard_scale", methods=["POST"])
def hard_scale():
    title = request.form.get('w_title')
    extractor.hard_scale(title)
    return redirect(url_for("learn_front"))


@app.route("/create_card", methods=["POST"])
def create_card():
    user_input = request.form.get("inputText")
    result = extractor.get_definition(user_input)
    extractor.save_word(result)
    print(result)
    if len(result) == 6:
        message = "added"
    elif result == "Word already in dictionary":
        message = "exists"
    elif result == "Unable to find":
        message = "wrong word"
    return render_template("create.html", message=message, word=user_input)


if __name__ == "__main__":
    app.run(debug=True)
