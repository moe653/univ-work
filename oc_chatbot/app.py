# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
import os

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
# セッション（ユーザーの状態を保存するため）のための秘密鍵を設定
# 本番環境では、より複雑で予測不能な値を設定してください
app.secret_key = os.urandom(24) 


# --- 研究室に関する情報の定義 ---
LAB_INFO = {
    "1": {
        "question" : "研究室の場所はどこですか？",
        "answer" : "当研究室は，高知工科大学香美キャンパスのA棟A358にあります．"
    },
    "2": {
        "question" : "研究室には何人の学生がいますか？",
        "answer" : "現在約20人の学生が在籍しています．"
    }
}

# --- 補助関数 ---
def get_answer_from_selection(choice):
    """選択された質問に対する回答を返す関数"""
    if choice in LAB_INFO:
        return LAB_INFO[choice]["answer"]
    else:
        return "申し訳ありませんが、その質問は選択肢にありません。再度選択してください。"

# --- ルート（URLとPython関数のマッピング）の設定 ---

# "/" にアクセスがあったときに実行される関数
@app.route("/", methods=["GET", "POST"])
def home():
    # 新しいセッション開始時にチャット履歴をクリア
    session.clear() 
    # チャット履歴を初期化
    session['chat_history'] = []
    # lab_infoをテンプレートに渡して、index.htmlを表示
    return render_template("index.html", lab_info=LAB_INFO, chat_history=session['chat_history'])

# "/chat" にPOSTリクエストがあったときに実行される関数
@app.route("/chat", methods=["POST"])
def chat():
    user_choice = request.form['question_choice'] # ユーザーが選択した質問の番号を取得
    user_question_text = LAB_INFO[user_choice]["question"] # 選択された質問のテキストを取得

    # チャット履歴をセッションから取得、なければ初期化
    chat_history = session.get('chat_history', [])

    # ユーザーの質問を履歴に追加
    chat_history.append({'speaker': 'user', 'speaker_label': 'あなた', 'text': user_question_text})

    # 回答を取得
    answer = get_answer_from_selection(user_choice)

    # チャットボットの回答を履歴に追加
    chat_history.append({'speaker': 'bot', 'speaker_label': 'チャットボット', 'text': answer})

    # 更新された履歴をセッションに保存
    session['chat_history'] = chat_history

    # テンプレートにデータを渡してindex.htmlを再表示
    return render_template("index.html", lab_info=LAB_INFO, chat_history=chat_history)

# --- アプリケーションの実行 ---
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)