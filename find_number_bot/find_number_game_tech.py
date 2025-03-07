import random 


#Количества попыток, доступных пользователю в игре
ATTEMPTS = 5


# Функция возвращающая случайное целое цисло от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# File ID стикера (замени на реальный)
STICKER_ID = "CAACAgIAAxkBAAICKGfFl2yV7-7VAAHz8US_hs67xRXdkAAChxUAAiMAAaBLV73BzYKM-wI2BA"