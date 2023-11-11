import os

import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
import logging

import convert_audio_in_text

logging.basicConfig(level=logging.INFO,
                    filename="py_log_BotGPT.log",
                    filemode="w")

load_dotenv()

openai.api_key = os.getenv('TOKEN_AI')


bot = Bot(os.getenv('TOKEN_BOT'))
dp = Dispatcher(bot)
dialog_history = {}


@dp.message_handler(content_types= types.ContentType.VOICE)
async def handle_message(message: types.Message):
    # global dialog_history
    # user_id = message.from_user.id
    # user_dialog_history = dialog_history.get(user_id, [])
    # user_dialog_history.append(message.text)
    # full_dialog = '\n'.join(user_dialog_history)
    # logging.info(f'{message.from_user}: {message.text}')
    # chat = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a bot"},
    #         {"role": "user", "content": full_dialog}
    #     ]
    # )
    # user_dialog_history.append(chat.choices[0].message.content)
    # dialog_history[user_id] = user_dialog_history
    # reply = chat.choices[0].message.content
    # logging.info(f'{reply}')
    file_voice = await bot.get_file(message.voice.file_id)
    file_path = file_voice.file_path
    download_file = await bot.download_file(file_path)
    convert_text = convert_audio_in_text.convert_text(download_file)
    await message.reply(convert_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
