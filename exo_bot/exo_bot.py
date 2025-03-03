"""
Начнем с самого простого - напишем бота, который будет на наши сообщения отвечать нашими же сообщениями и на его примере рассмотрим самый простой шаблон.
"""

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from private_for_API import BOT_TOKEN


#создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def procress_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что нибуть')

# этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def procress_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибуть и в ответ  '
        'я пришлю тебе твое сообщение'
    )

# Этот хендлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команды "/start" и  "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)

