# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# --- ルート（URLとPython関数のマッピング）の設定 ---
# "/" にアクセスがあったときに実行される関数
@app.route("/")
def home():
    return "<h1>Hello, World! This is my Lab Chatbot Web App!</h1>"

# --- アプリケーションの実行 ---
if __name__ == "__main__":
    # デバッグモードを有効にしてアプリケーションを実行
    # WSLで外部からアクセスできるようにhost='0.0.0.0'を設定
    app.run(debug=True, host='0.0.0.0', port=5000)