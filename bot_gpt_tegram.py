import os

import g4f
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
import logging


import convert_audio_in_text

logging.basicConfig(level=logging.INFO,
                    filename="py_log_BotGPT.log",
                    filemode="w")

load_dotenv()



bot = Bot(os.getenv('TOKEN_BOT'))
dp = Dispatcher(bot)
conversation_history = {}

def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history

@dp.message_handler()
async def handle_message_other(message: types.Message):
    #Берем текст из сообщения
    convert_text = message.text
    user_id = message.from_user.id
    user_input = convert_text
    # Проверка наличия пользователя в диалоге
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    # Добавления сообщения пользователя в диалог
    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history = conversation_history[user_id]
    # Создание gpt запроса
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        messages=chat_history,
        provider=g4f.Provider.GeekGpt,
    )
    chat_gpt_response = response
    # Добавления ответа в историю диалога
    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    await message.answer(chat_gpt_response)


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_message(message: types.Message):
    #Обработка голосового и представление его в виде текста.
    file_voice = await bot.get_file(message.voice.file_id)
    file_path = file_voice.file_path
    download_file = await bot.download_file(file_path)
    convert_text = await convert_audio_in_text.convert_text(download_file)
    user_id = message.from_user.id
    user_input = convert_text
    #Проверка наличия пользователя в диалоге
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    #Добавления сообщения пользователя в диалог
    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history = conversation_history[user_id]
    #Создание gpt запроса
    response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=chat_history,
            provider=g4f.Provider.GeekGpt,
        )
    chat_gpt_response = response
    #Добавления ответа в историю диалога
    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    await message.answer(chat_gpt_response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
