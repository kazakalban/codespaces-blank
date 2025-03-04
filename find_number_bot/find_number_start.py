from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from private_for_API import BOT_TOKEN


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# этот хендлер будет срабатывать на команду "/start"
@dp.message(Command("start"))
async def start_hendler(message: Message):
    await message.answer('hi')

if __name__ == '__main__':
    dp.run_polling(bot)