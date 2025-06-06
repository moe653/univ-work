# 質問の内容とその回答を定義
# 質問の内容とその回答を辞書形式で管理
# キーは質問の番号，値は質問の内容と回答を含む別の辞書
LAB_INFO = {
    "1": {
        "question" : "研究室の場所はどこですか？",
        "answer" : "敷田研究室は，高知工科大学香美キャンパスのA棟A358にあります．"
    },
    "2": {
        "question" : "研究室には何人の学生がいますか？",
        "answer" : "現在約20人の学生が在籍しています．"
    }
}

def display_menu():
    # 質問の選択肢を表示する関数
    print("\n---研究室チャットボット---")
    print("質問を選択してください（番号を入力）：")
    for num, info in LAB_INFO.items():
        print(f"{num}. {info['question']}")
    print("0. 終了する");
    print("-------------------")

def get_answer_from_selection(choice):
    """選択された質問に対する回答を返す関数"""
    if choice in LAB_INFO:
        return LAB_INFO[choice]["answer"]
    else:
        return "申し訳ありませんが、その質問は選択肢にありません。再度選択してください。"

def chat_bot_manual_selection():
    """手動稼働・選択肢形式のチャットボット本体"""
    print("チャットボットを開始します。")

    while True: # 無限ループ
        display_menu() # メニューを表示
        user_input = input("あなたの選択: ") # ユーザーからの入力を受け取る

        if user_input == "0":
            print("チャットボットを終了します。ありがとうございました！")
            break # ループを抜けてプログラムを終了
        else:
            answer = get_answer_from_selection(user_input) # 回答を取得
            print(f"\nチャットボット: {answer}") # 回答を表示

# --- メイン処理 ---
# このスクリプトが直接実行された場合にのみ、chat_bot_manual_selection()関数を呼び出す
if __name__ == "__main__":
    chat_bot_manual_selection()
