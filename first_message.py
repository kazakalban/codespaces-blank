import requests
import time 
from private_for_API import API_URL, BOT_TOKEN, TEXT, MAX_COUNTER

offset = -2
counter = 0
chat_id: int

while counter < MAX_COUNTER:
    print('attemp =', counter) # Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
    time.sleep(1)
    counter += 1