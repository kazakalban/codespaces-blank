from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from private_for_API import BOT_TOKEN


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Навешиваем декораторы с указанием в качестве фильтра типа контента 
@dp.message(F.voice)
async def process_sent_voice(message: Message):
    print(message)
    # Отправляем в чат, откуда пришло сообщение!
    await message.answer(text='Вы прислали голосовое сообщение!')

if __name__ == '__main__':
    dp.run_polling(bot)