# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
import os
import csv 
from collections import defaultdict 

app = Flask(__name__)
app.secret_key = os.urandom(24) 

# --- 研究室に関する情報の定義 ---
def load_lab_info_from_csv(filepath='lab_info.csv'):
    lab_info = {}
    categorized_lab_info = defaultdict(dict) 
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # CSVのidをキーとして、question, answer, genreを辞書として保存
                lab_info[row['id']] = {
                    "question": row['question'],
                    "answer": row['answer'],
                    "genre": row.get('genre', 'その他') 
                }
                # ジャンルごとに質問をグループ化
                categorized_lab_info[row.get('genre', 'その他')][row['id']] = {
                    "question": row['question'],
                    "answer": row['answer']
                }
        print(f"CSVファイル '{filepath}' から情報を読み込みました。")
    except FileNotFoundError:
        print(f"エラー: '{filepath}' が見つかりませんでした。")
        print("ダミーデータを使用します。")
        lab_info = {
            "1": {"question": "ダミー質問1？", "answer": "ダミー回答1です。", "genre": "その他"},
            "2": {"question": "ダミー質問2？", "answer": "ダミー回答2です。", "genre": "その他"}
        }
        categorized_lab_info["その他"] = {
            "1": {"question": "ダミー質問1？", "answer": "ダミー回答1です。"},
            "2": {"question": "ダミー質問2？", "answer": "ダミー回答2です。"}
        }
    except Exception as e:
        print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        print("ダミーデータを使用します。")
        lab_info = {
            "1": {"question": "ダミー質問1？", "answer": "ダミー回答1です。", "genre": "その他"},
            "2": {"question": "ダミー質問2？", "answer": "ダミー回答2です。", "genre": "その他"}
        }
        categorized_lab_info["その他"] = {
            "1": {"question": "ダミー質問1？", "answer": "ダミー回答1です。"},
            "2": {"question": "ダミー質問2？", "answer": "ダミー回答2です."}
        }

    return lab_info, categorized_lab_info

LAB_INFO, CATEGORIZED_LAB_INFO = load_lab_info_from_csv()

# --- 補助関数 ---
def get_answer_from_selection(choice):
    """選択された質問に対する回答を返す関数"""
    if choice in LAB_INFO:
        return LAB_INFO[choice]["answer"]
    else:
        return "申し訳ありませんが、その質問は選択肢にありません。再度選択してください。"

# --- ルート（URLとPython関数のマッピング）の設定 ---

# トップページ。ジャンル選択ボタンを表示する。
@app.route("/", methods=["GET", "POST"])
def home():
    session.clear() 
    session['chat_history'] = []
    # ジャンルのリストをテンプレートに渡す
    # CATEGORIZED_LAB_INFO.keys() でジャンル名のみを取得
    return render_template("index.html", genres=CATEGORIZED_LAB_INFO.keys(), chat_history=session['chat_history'])

# ジャンルが選択されたときに呼び出される新しいルート
@app.route("/select_genre", methods=["POST"])
def select_genre():
    selected_genre = request.form['genre_choice'] # ユーザーが選択したジャンル名を取得

    # 選択されたジャンルの質問リストをテンプレートに渡す
    # ここではchat_historyは引き継がず、新たなチャットが始まるイメージ
    questions_in_genre = CATEGORIZED_LAB_INFO.get(selected_genre, {})

    # 選択されたジャンルをセッションに保存（後でチャット履歴表示のために使う可能性も考慮）
    session['selected_genre'] = selected_genre 

    # ジャンル内の質問を表示するためのテンプレートをレンダリング
    return render_template("genre_questions.html", 
                           genre_name=selected_genre, 
                           questions=questions_in_genre,
                           chat_history=session['chat_history'])

# 質問が選択されたときに呼び出されるルート
@app.route("/chat", methods=["POST"])
def chat():
    user_choice = request.form['question_choice'] 
    user_question_text = LAB_INFO.get(user_choice, {}).get("question", "不明な質問")

    chat_history = session.get('chat_history', [])

    chat_history.append({'speaker': 'user', 'speaker_label': 'あなた', 'text': user_question_text})

    answer = get_answer_from_selection(user_choice)

    chat_history.append({'speaker': 'bot', 'speaker_label': 'チャットボット', 'text': answer})

    session['chat_history'] = chat_history

    # 質問選択後もジャンル内の質問ボタンを表示するために、同じジャンルを再度渡す
    # 選択されたジャンルをセッションから取得
    selected_genre = session.get('selected_genre', '不明なジャンル') 
    questions_in_genre = CATEGORIZED_LAB_INFO.get(selected_genre, {})

    return render_template("genre_questions.html", 
                           genre_name=selected_genre, 
                           questions=questions_in_genre, 
                           chat_history=chat_history)

# --- アプリケーションの実行 ---
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)