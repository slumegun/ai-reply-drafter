from pyrogram import compose

from bot import bot_client
from userbot import userbot_client
from database import chat_bd, predicted_messages_bd


def main():
    try:
        compose([userbot_client, bot_client])
    finally:
        predicted_messages_bd.close()
        chat_bd.close()
        print("databases are closed.")

if __name__ == "__main__":
    main()
