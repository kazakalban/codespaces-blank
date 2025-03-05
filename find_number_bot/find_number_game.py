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


#Создаем объекты бота 
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

#Количества попыток, доступных пользователю в игре
ATTEMPTS = 5

#Словарь в котором будет храниться данные пользователя
user = {'in_game':False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}

# File ID стикера (замени на реальный)
STICKER_ID = "CAACAgIAAxkBAAICKGfFl2yV7-7VAAHz8US_hs67xRXdkAAChxUAAiMAAaBLV73BzYKM-wI2BA"

# Функция возвращающая случайное целое цисло от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

#@dp.message()
#async def get_sticker_id(message: Message):
#    if message.sticker:
#        await message.answer(f"Вот твой file_id:\n{message.sticker.file_id}")


# Этот хендлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await bot.send_sticker(message.chat.id, STICKER_ID)
    await message.answer(
        '👋 Привет!\n\n🎲 Давайте сыграем в игру *"Угадай число"!*🔢\n\n'
        '📜 Чтобы получить правила игры и список доступных команд,' 
        'отправьте команду /help 🆘',
        parse_mode='Markdown'
    )


# Этот хендлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def proccess_help_command(message:Message):
    await message.answer(
        "🎯 *Правила игры:*\n\n"
        "🤖 Я загадываю число от *1 до 100*, а вам нужно его угадать! 🔢\n"
        f"🎌 У вас есть *{ATTEMPTS}* попыток!\n\n"
        "📜 *Доступные команды:*\n"
        "🆘 /help - правила игры и список команд\n"
        "❌ /cancel - выйти из игры\n"
        "📊 /stat - посмотреть статистику\n\n"
        "🔥 Давай сыграем? 😃\n"
        "💬 Если хочешь играть, напиши: *да*, *давай*, *сыграем*, *игра*, *играть*, *хочу играть*! 🎮",
        parse_mode='Markdown'
    )

# Этот хендлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message:Message):
    await message.answer(
        f"📊 *Ваша статистика:*\n\n"
        f"🎮 *Всего игр сыграно:* {user['total_games']}\n"
        f"🏆 *Игр выиграно:* {user['wins']}\n\n"
        "Продолжим игру? 🔥",
        parse_mode="Markdown"
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def proccess_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            "❌ *Вы вышли из игры.*\n\n"
            "😌 Отдохните, но если захотите сыграть снова — просто напишите"
            " *да*, *давай*, *сыграем* или *игра*! 🎮🔥",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "🤔 *А мы и так с вами не играем.*\n\n"
            "🎲 Может, сыграем разок? Будет весело! 🔥\n"
            "Напишите *да*, *давай*, *сыграем* или *игра*, чтобы начать! 🎮",
            parse_mode="Markdown"        
        )


# Этот хендлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_ ['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть'])
async def proccess_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )





if __name__ == '__main__':
    dp.run_polling(bot)