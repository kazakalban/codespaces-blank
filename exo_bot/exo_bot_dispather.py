from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from private_for_API import BOT_TOKEN 


#Создаем объекты бота и диспетчера
bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду "/start"
async def procces_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибуть')

# Этот хэндлер будет срабатывать на команду "/help"
async def procces_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибуть и в ответ\n'
        'я пришлю тебе твое сообщение'
    )

# Этот хендлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команды "/start" и "/help"
async def send_echo(message: Message):
    await message.reply(text=message.text)

# Регистрируем хэндлеры
dp.message.register(procces_start_command, Command(commands = 'start'))
dp.message.register(procces_help_command, Command(commands = 'help'))
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)

