from pyrogram import Client, filters
from pyrogram.raw import functions
import asyncio

import os
from dotenv import load_dotenv

from bot import send_answer
from database import chat_bd, predicted_messages_bd


load_dotenv()

hostname = os.getenv('hostname')
port = int(os.getenv('port'))
username = os.getenv('proxy_username')
password = os.getenv('proxy_password')
api_hash = os.getenv('api_hash')
api_id = int(os.getenv('api_id'))

friend_name = os.getenv('friend_name') # Username of your friend

proxy = dict(
    scheme='http',
    hostname=hostname,
    port=port,
    username=username,
    password=password
)

userbot_client = Client(api_hash=api_hash, api_id=api_id, proxy=proxy, lang_code="ru", name="my_account")

###############################################################################################

@userbot_client.on_message(filters.incoming & filters.text & filters.private)
async def get_message(client, message):
    msg = message.text
    date = message.date

    if message.from_user.username == friend_name:
        chat_bd.add_message(message=msg, date=date, person="user")
        await message_handling.saving_message(msg, date)

@userbot_client.on_message(filters.text & filters.outgoing & filters.private)
async def save_message_to_bd(client, message):
    msg = message.text
    date = message.date

    if message.chat.username == friend_name:
            chat_bd.add_message(message=msg, date=date, person="assistant")

async def create_draft(message: str) -> None:
    await userbot_client.invoke(
        functions.messages.SaveDraft(
            peer=await userbot_client.resolve_peer(friend_name),
            message=message
        )
    )

class MessagesHandling:
    def __init__(self):
        self.timer = None
        self.messages = None

    async def saving_message(self, msg: str, date):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

        if self.messages is not None:
            self.messages = self.messages + " | " + msg
        else:
            self.messages = msg

        self.timer = asyncio.create_task(self.respond(date))

    async def respond(self, date):
        await asyncio.sleep(3)

        chat_history = chat_bd.get_chat_history(date=date)
        answer, message_id = await send_answer(self.messages, chat_history=chat_history)

        predicted_messages_bd.add_message(predicted_text=answer, date=date, message_id=message_id)

        self.messages = None

message_handling = MessagesHandling()        
