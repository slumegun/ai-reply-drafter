from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import os
from dotenv import load_dotenv

from model import Generating
from database import predicted_messages_bd


load_dotenv()

hostname = os.getenv('hostname')
port = int(os.getenv('port'))
username = os.getenv('proxy_username')
password = os.getenv('proxy_password')
api_hash = os.getenv('api_hash')
api_id = int(os.getenv('api_id'))
bot_token = os.getenv('bot_token')
friend_name = os.getenv('friend_name')
my_id = int(os.getenv('my_id'))

proxy = dict(
    scheme='http',
    hostname=hostname,
    port=port,
    username=username,
    password=password
)

bot_client = Client(name="bot", api_hash=api_hash, api_id=api_id, proxy=proxy, lang_code="ru", bot_token=bot_token)

########################################################################################################################

@bot_client.on_callback_query()
async def callback_handler(client, callback_query):
    from userbot import create_draft

    await callback_query.answer()

    num = int(callback_query.data.split("_")[1])
    predicted_messages_bd.set_used(message_id=callback_query.message.id)

    await create_draft(message=callback_query.message.text.split("|")[num-1])

async def send_answer(msgs: str, chat_history):
    answer = await asyncio.to_thread(model.generate_answer, msgs, chat_history)

    answers = answer.split("|")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"draft {i+1}", callback_data=f"draft_{i+1}") for i in range(len(answers))]])

    message_id = str((await bot_client.send_message(my_id, answer, reply_markup=keyboard)).id)

    return answer, message_id

model = Generating()
