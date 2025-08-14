import json
import sys
import os
import asyncio
from pyrogram import Client, errors
from random import randint, choice
module_dir = rf"{os.path.dirname(os.path.abspath(__file__))}/bomber/"
sys.path.insert(0, module_dir)
from msg import msgforspam

with open(rf"{module_dir}botnet.json") as f:
    bots = json.load(f)['bots']

usernames = []
with open(rf"{module_dir}usernames.txt") as unames:
    for username in unames.readlines():
        usernames.append(username)

sessions = []

async def send(client, username):
    try:
        msg = msgforspam(number, randint(0, 3))
        await client.send_message(username, msg)
        print(f"sent: {client.name} -> {username}")
        return True
    except errors.UserPrivacyRestricted:
        print(f"privacy error: {username}")
    except errors.UserIsBlocked:
        print(f"blocked: {client.name}")
    except errors.PeerIdInvalid:
        print(f"invalid peer: {username}")
    except Exception as e:
        print(f"error: {type(e).__name__}")
    return False

async def run():
    for bot in bots:
        if bot['work']:
            client = Client(
                bot['session'],
                api_id=bot["api_id"],
                api_hash=bot["api_hash"],
                phone_number=bot["phone"]
            )
            sessions.append(client)
            await client.start()
    
    for username in usernames:
        client = choice(sessions)
        if await send(client, username):
            await asyncio.sleep(randint(5, 10))
        else:
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        for client in sessions:
            if client.is_initialized:
                asyncio.run(client.stop())
        print("terminated")
