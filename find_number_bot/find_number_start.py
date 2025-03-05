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
    await message.answer('Чтобы Согласиться поиграть с ботом в игру, отправив в чат "Да" или "Давай", или "Сыграем"')

# этот хендлер будет срабатывать на команду "/help"
@dp.message(Command("help"))
async def help_hendler(message: Message):
    await message.answer('Помощь')

@dp.message()
async def agree_game(message: Message):
    if message.text.lower() in ["да","давай","сыграем"]:
        await message.answer(text="Игра начинается!!!")
    elif message.text.lower() in [ "нет","не хочу","в другой раз"]:
        await message.answer(text="Игра не начинается!!!")
    else:
        await message.answer(text="Я не понял тебя")

if __name__ == '__main__':
    dp.run_polling(bot)