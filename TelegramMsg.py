import requests
import os

chat_id = os.getenv('TELEGRAM_CHAT_ID')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response.json()

def send_telegram_image(image_path: str, caption: str = ''):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {
            'chat_id': chat_id,
            'caption': caption
        }
        response = requests.post(url, files=files, data=data)

    print(f"Telegram response: {response.status_code}")
    return response.json()

def save_and_send_plot(fig, filename='chart.png', caption='📈 Stock chart'):
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    response = send_telegram_image(filename, caption=caption)
    os.remove(filename)  # delete the image after sending
    return response