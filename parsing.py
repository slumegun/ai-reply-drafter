from pyrogram import Client

from dotenv import load_dotenv
import os
import json


load_dotenv()

hostname = os.getenv('hostname')
port = int(os.getenv('port'))
username = os.getenv('proxy_username')
password = os.getenv('proxy_password')
api_hash = os.getenv('api_hash')
api_id = int(os.getenv('api_id'))

name = '@' + os.getenv('friend_name') # Username or id of your friend

proxy = dict(
    scheme="http",
    hostname=hostname,
    port=port,
    username=username,
    password=password
)

client = Client(api_hash=api_hash, api_id=api_id, proxy=proxy, lang_code="ru", name="my_account")


#######################################################################


class FileSystem:
    def __init__(self):
        self.dataset = []

    def dataset_append(self, friend_msg: str, my_msg: str):
        example = {"messages": [{"role": "user", "content": friend_msg}, {"role": "assistant", "content": my_msg}]}
        self.dataset.append(example)

    def write_to_file(self):
        with open("dataset.jsonl", "a", encoding="utf-8") as f:
            for example in self.dataset:
                f.write(json.dumps(example, ensure_ascii=False) + "\n")
            self.dataset = []


file_system = FileSystem()

class ParsSystem:
    def __init__(self):
        self.friend_messages = []
        self.my_messages = []
        self.last_message = None

    async def parse(self):
        my_id = (await client.get_me()).id
        counter = 0
        async for message in client.get_chat_history(name, offset=0):
                counter+=1
                if counter%1000 == 0:
                    print("Messages checked: ", counter)
                msg = message.text
                if msg is not None:
                    if message.from_user.id == my_id:
                        if self.last_message == None:
                            self.last_message = "mine"
                        elif self.last_message != "mine":
                            self.my_messages.reverse()
                            my_msg = " | ".join(self.my_messages)
                            self.my_messages = []
                            self.friend_messages.reverse()
                            friend_msg = " | ".join(self.friend_messages)
                            self.friend_messages = []
                            file_system.dataset_append(my_msg=my_msg, friend_msg=friend_msg)
                            if len(file_system.dataset) >= 100:
                                file_system.write_to_file()
                            self.last_message = "mine"
                        self.my_messages.append(msg)
                    else:
                        if self.last_message == None:
                            continue
                        self.friend_messages.append(msg)
                        if self.last_message == "mine":
                            self.last_message = "not mine"
        file_system.write_to_file()


pars_system = ParsSystem()

async def main():
    async with client:
        await pars_system.parse()
        print("Done!")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
