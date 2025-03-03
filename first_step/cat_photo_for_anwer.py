import requests 
import time 
from private_for_API import API_URL, API_CATS_URL, BOT_TOKEN, ERROR_TEXT, TEXT

offset = -2 
counter = 0
cat_response: requests.Response
cat_link: str

while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            user_text = result['message']['text']
            user_first_name = result['message']['from']['first_name']
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={user_text} это я понимаю, но {user_first_name} перестань!')
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}&text={TEXT}')
    time.sleep(1)
    counter += 1