#!/usr/bin/env python3

import os
import re
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient, sync, events

load_dotenv()

today = datetime.today()

client = TelegramClient('anon', os.getenv('API_ID'), os.getenv('API_HASH'))
client.start()

print('date', 'usage', 'installed', 'removed', sep=',')


@client.on(events.NewMessage(chats='Stickers', pattern='^Stats for the sticker pack (.+?) for'))
async def handler(event):
    m = re.search(
        r'([0-9]{2}\/[0-9]{2}\/[0-9]{4}):\n+Usage: ([0-9]+)\nInstalled: ([0-9]+)\nRemoved: ([0-9]+)\n',
        event.message.message,
    )
    date = datetime.strptime(m.group(1), '%m/%d/%Y')
    print(date.date(), m.group(2), m.group(3), m.group(4), sep=',')

    if date.date() == today.date():
        await client.disconnect()

client.send_message('Stickers', '/cancel')
client.send_message('Stickers', '/packstats')
client.send_message('Stickers', sys.argv[1])
time.sleep(1)

for days in range(356, -1, -1):
    date = today - timedelta(days)
    client.send_message('Stickers', date.strftime('%m/%d/%Y'))

client.run_until_disconnected()
