import requests
import time
from datetime import datetime

# আপনার config
IVAS_API_URL = 'http://localhost:5000/sms'  # আপনার IVAS API endpoint (localhost বা server URL)
TELEGRAM_BOT_TOKEN = '8282428157:AAEGhPLCnG-YJxhdCM2JOzV-0GvZX_QhZdY'  # BotFather থেকে
TELEGRAM_CHAT_ID = '-1002953835150'  # গ্রুপের chat ID
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# আগের চেকের তারিখ track করার জন্য (সিম্পলভাবে file-এ সেভ করুন)
LAST_CHECK_DATE = '15/09/2025'  # শুরুতে আজকের তারিখ দিন

def get_sms_from_ivas():
    params = {'date': datetime.now().strftime('%d/%m/%Y')}  # আজকের তারিখ
    response = requests.get(IVAS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('otp_messages', [])  # OTP messages list
    return []

def send_to_telegram(message):
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'  # Optional, formatting-এর জন্য
    }
    requests.post(TELEGRAM_API_URL, data=payload)

# Main loop
while True:
    sms_list = get_sms_from_ivas()
    for sms in sms_list:
        phone = sms.get('phone_number', 'Unknown')
        otp_msg = sms.get('otp_message', 'No message')
        full_msg = f"নতুন OTP/SMS এসেছে!\nফোন: {phone}\nমেসেজ: {otp_msg}\nসময়: {datetime.now()}"
        send_to_telegram(full_msg)
        print(f"Sent: {full_msg}")
    
    time.sleep(60)  # ১ মিনিট পর পর চেক করুন (OTP-এর জন্য যথেষ্ট)