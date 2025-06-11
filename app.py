from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = [
    {"question": "ムーンさんはええやつ過ぎてがーさすに？", "options": ["なくぅ", "おおすこでぇすこ", "ええやつすぎるやんすぎるやん", "わらじん"], "answer": "なくぅ"},
    {"question": "さむら？", "options": ["あ", "い", "う", "え"], "answer": "い"},
    {"question": "かつやは？", "options": ["将軍", "関白", "師匠", "ざむらい"], "answer": "師匠"}
]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session.clear()
        session["username"] = request.form["username"]
        session["current"] = 0
        session["score"] = 0
        session["answers"] = []
        return redirect(url_for("quiz"))
    return render_template("index.html")  # 新規作成

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
    session["current"] = current + 1
    return render_template("quiz_one.html", question=q, index=current + 1, total=len(questions))

@app.route("/result")
def result():
    score = session.get("score", 0)
    answers = session.get("answers", [])
    username = session.get("username", "匿名")

    # --- ランキング保存処理 ---
    try:
        with open("ranking.json", "r", encoding="utf-8") as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []

    ranking.append({"name": username, "score": score})
    ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)[:5]

    with open("ranking.json", "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

    result_data = list(zip(questions, answers))
    return render_template("result_with_review.html", score=score, total=len(questions), result_data=result_data, ranking=ranking)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
