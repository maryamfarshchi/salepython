from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import requests

app = Flask(__name__)

# تنظیمات Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# لینک شیت و نام شیت
spreadsheet = client.open("clever. sale")  # نام فایل گوگل شیتت
sheet = spreadsheet.sheet1("مصرف کنندگان")  # یا .worksheet("نام دقیق شیت")

# توکن ربات تلگرام
BOT_TOKEN = "8190481116:AAFWPwhwHufySrziUFaQVOEiBvRc-Bk52OU"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "callback_query" in data:
        cb = data['callback_query']
        user = cb['from']['first_name']
        chat_id = cb['message']['chat']['id']
        callback_data = cb['data']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ثبت در گوگل شیت
        sheet.append_row([timestamp, user, chat_id, callback_data])

        # پاسخ به کلیک
        answer_callback(cb['id'], "ثبت شد 🌿")

    return "ok"

def answer_callback(callback_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    payload = {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": False
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
