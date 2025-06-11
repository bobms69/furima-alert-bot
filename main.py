import requests
import time

# ゆうとのTelegram Botの情報
BOT_TOKEN = "7516151948:AAFlbSGnymovHmMcEPs9VBFgA1r5HwkZ5t4"
CHAT_ID = "7993770668"

# 通知対象の検索ワード
KEYWORDS = ["クロコ バッグ", "オーストリッチ バッグ"]

# メルカリの検索URLテンプレート（Web版）
def build_search_url(keyword):
    return f"https://www.mercari.com/jp/search/?keyword={keyword}&sort_order=created_time&status=on_sale"

# 過去に通知したURLを保存する（重複防止）
notified_urls = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.ok

def check_mercari():
    for keyword in KEYWORDS:
        search_url = build_search_url(keyword)
        try:
            res = requests.get(search_url)
            if keyword in res.text:
                if search_url not in notified_urls:
                    notified_urls.add(search_url)
                    send_telegram_message(f"🔍 新着あり！\n{keyword}\n{search_url}")
        except Exception as e:
            print(f"エラー発生: {e}")

if __name__ == "__main__":
    while True:
        check_mercari()
        time.sleep(300)  # 5分おきにチェック（変更OK）
