"""
Игра "Угадай число" для одного пользователя
Давайте для простоты пока предположим, что у нас всего один пользователь бота. 
Нам понадобится хранить следующие данные:

Состояние "Игра" или "Не игра"
Загаданное ботом число
Количество оставшихся у пользователя попыток
Сколько всего было игр у пользователя
В скольких играх пользователь выиграл
"""

import random 

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from private_for_API import BOT_TOKEN
import find_number_game_text as texts
from find_number_game_user_bd import user
                                    


#Создаем объекты бота 
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

#Количества попыток, доступных пользователю в игре
ATTEMPTS = 5

# File ID стикера (замени на реальный)
STICKER_ID = "CAACAgIAAxkBAAICKGfFl2yV7-7VAAHz8US_hs67xRXdkAAChxUAAiMAAaBLV73BzYKM-wI2BA"

# Функция возвращающая случайное целое цисло от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Этот хендлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await bot.send_sticker(message.chat.id, STICKER_ID)
    await message.answer(
        texts.START_TEXT,
        parse_mode='Markdown'
    )


# Этот хендлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def proccess_help_command(message:Message):
    await message.answer(
        texts.HELP_TEXT.format(ATTEMPTS = ATTEMPTS),
        parse_mode='Markdown'
    )


# Этот хендлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message:Message):
    await message.answer(
        texts.STAT_TEXT.format(total_games = user['total_games'],
                         wins = user['wins']),
        parse_mode="Markdown"
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def proccess_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            texts.CANCEL_TEXT,
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            texts.CANCEL_TEXT_ELSE,
            parse_mode="Markdown"        
        )


# Этот хендлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_ (['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def proccess_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        print(user['secret_number'])
        user['attempts'] = ATTEMPTS
        await message.answer(
            texts.POSITIVE_ANSWER_TEXT
        )
    else:
        await message.answer(
            texts.POSITIVE_ANSWER_TEXT_ELSE 
        )


# Этот хендлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1<= int(x.text) <= 100)
async def proccess_number_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer(
                texts.NUMBER_ANSWER_TEXT,
                parse_mode="Markdown"
            )
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Мое число больше')
        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                texts.NUMBER_ANSWER_TEXT_NO_LIFE.format(secret_number = user['secret_number']),
                parse_mode="Markdown"
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хендлер будет срабатывать на остальные любые соощения
@dp.message()
async def proccess_other_answers(message: Message):
        if user['in_game']:
            await message.answer(
                texts.OTHER_ANSWER_TEXT,
                parse_mode = "Markdown"
            )
        else:
            await message.answer(
                texts.OTHER_ANSWER_TEXT_ELSE,
                parse_mode="Markdown"
            ) 


# Этот хендлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_ (['нет', 'не', 'не хочу', 'не буду']))
async def proccess_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            texts.NO_ANSWER_TEXT,
            parse_mode = "Markdown"
        )
    else:
        await message.answer(
            texts.OTHER_ANSWER_TEXT,
            parse_mode="Markdown"
        )


if __name__ == '__main__':
    dp.run_polling(bot)