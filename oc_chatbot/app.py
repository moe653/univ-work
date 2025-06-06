# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
import os
import csv # CSVファイルを扱うために追加

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
# セッション（ユーザーの状態を保存するため）のための秘密鍵を設定
app.secret_key = os.urandom(24) 

# --- 研究室に関する情報の定義 ---
# LAB_INFOをCSVから読み込む関数
def load_lab_info_from_csv(filepath='lab_info.csv'):
    lab_info = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # CSVのidをキーとして、questionとanswerを辞書として保存
                lab_info[row['id']] = {
                    "question": row['question'],
                    "answer": row['answer']
                }
        print(f"CSVファイル '{filepath}' から情報を読み込みました。")
    except FileNotFoundError:
        print(f"エラー: '{filepath}' が見つかりませんでした。")
        print("ダミーデータを使用します。")
        # ファイルが見つからない場合のダミーデータ（開発用）
        lab_info = {
            "1": {"question": "ダミー質問1？", "answer": "ダミー回答1です。"},
            "2": {"question": "ダミー質問2？", "answer": "ダミー回答2です。"}
        }
    except Exception as e:
        print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        print("ダミーデータを使用します。")
        lab_info = {
            "1": {"question": "ダミー質問1？", "answer": "ダミー回答1です。"},
            "2": {"question": "ダミー質問2？", "answer": "ダミー回答2です。"}
        }
    return lab_info

# アプリケーション起動時にCSVから情報を読み込む
LAB_INFO = load_lab_info_from_csv()

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
    session.clear() 
    session['chat_history'] = []
    return render_template("index.html", lab_info=LAB_INFO, chat_history=session['chat_history'])

# "/chat" にPOSTリクエストがあったときに実行される関数
@app.route("/chat", methods=["POST"])
def chat():
    user_choice = request.form['question_choice'] 

    # 選択された質問がLAB_INFOに存在するか確認し、存在しない場合はデフォルトの質問テキストを設定
    user_question_text = LAB_INFO.get(user_choice, {}).get("question", "不明な質問")

    chat_history = session.get('chat_history', [])

    chat_history.append({'speaker': 'user', 'speaker_label': 'あなた', 'text': user_question_text})

    answer = get_answer_from_selection(user_choice)

    chat_history.append({'speaker': 'bot', 'speaker_label': 'チャットボット', 'text': answer})

    session['chat_history'] = chat_history

    return render_template("index.html", lab_info=LAB_INFO, chat_history=chat_history)

# --- アプリケーションの実行 ---
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)