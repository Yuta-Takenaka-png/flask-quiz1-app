from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = [
    {"question": "ムーンさんはええやつ過ぎてがーさすに？", "options": ["なくぅ", "おおすこでぇすこ", "ええやつすぎるやんすぎるやん", "わらじん"], "answer": "なくぅ"},
    {"question": "さむら？", "options": ["あ", "い", "う", "え"], "answer": "い"},
    {"question": "かつやは？", "options": ["将軍", "関白", "師匠", "ざむらい"], "answer": "師匠"}
]

@app.route("/")
def home():
    session.clear()
    session["current"] = 0
    session["score"] = 0
    session["answers"] = []
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    current = session.get("current", 0)

    if request.method == "POST" and current > 0:
        selected = request.form.get("answer")
        session["answers"].append(selected)
        if selected == questions[current - 1]["answer"]:
            session["score"] += 1

    if current >= len(questions):
        return redirect(url_for("result"))

    q = questions[current]
    session["current"] = session.get("current", 0) + 1
    return render_template("quiz_one.html", question=q, index=current + 1, total=len(questions))

@app.route("/result")
def result():
    answers = session.get("answers", [])
    score = session.get("score", 0)
    result_data = list(zip(questions, answers))
    return render_template(
        "result_with_review.html",
        score=score,
        total=len(questions),
        result_data=result_data
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render が指定するポート番号を取得
    app.run(host="0.0.0.0", port=port, debug=True)
