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

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from private_for_API import BOT_TOKEN
import find_number_game_text as texts
from find_number_game_user_bd import users
from find_number_game_tech import ATTEMPTS,get_random_number,STICKER_ID
                                    


#Создаем объекты бота 
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# Этот хендлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await bot.send_sticker(message.chat.id, STICKER_ID)
    await message.answer(
        texts.START_TEXT,
        parse_mode='Markdown'
    )
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }

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
        texts.STAT_TEXT.format(total_games = users[message.from_user.id]['total_games'],
                        wins = users[message.from_user.id]['wins']),
        parse_mode="Markdown"
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def proccess_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
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
@dp.message(F.text.lower().in_ (texts.POSITIVE_ANSWER))
async def proccess_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        print(users[message.from_user.id]['secret_number'])
        users[message.from_user.id]['attempts'] = ATTEMPTS
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
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                texts.NUMBER_ANSWER_TEXT,
                parse_mode="Markdown"
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(texts.MY_NUMBER_LESS)
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(texts.MY_NUMBER_MORE)
        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                texts.NUMBER_ANSWER_TEXT_NO_LIFE.format(secret_number = users[message.from_user.id]['secret_number']),
                parse_mode="Markdown"
            )
    else:
        await message.answer(texts.NUMBER_ANSWER_TEXT_IN_GAME_FALSE)


# Этот хендлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_ (texts.NEGATIVE_ANSWER))
async def proccess_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            texts.NO_ANSWER_TEXT,
            parse_mode = "Markdown"
        )
    else:
        await message.answer(
            texts.OTHER_ANSWER_TEXT,
            parse_mode="Markdown"
        )


# Этот хендлер будет срабатывать на остальные любые соощения
@dp.message()
async def proccess_other_answers(message: Message):
        if users[message.from_user.id]['in_game']:
            await message.answer(
                texts.OTHER_ANSWER_TEXT,
                parse_mode = "Markdown"
            )
        else:
            await message.answer(
                texts.OTHER_ANSWER_TEXT_ELSE,
                parse_mode="Markdown"
            ) 


if __name__ == '__main__':
    dp.run_polling(bot)