import os
from typing import Union
from pyrogram import Client, types, enums, filters
from pyrogram.errors.exceptions import unauthorized_401
from colorama import Fore, Back, init as init_colorama
import asyncio
import sqlite3
import random
from threading import Thread
import json


init_colorama(autoreset=True)

api_id = 25629659
api_hash = "2a20c92ac50af0bc7f73c24d866b89d7"
my_id = 1870013463
main_chat_id = -1001696226781
auto_send_comment_chat_id = -1001578976976
screamers = 0
client_name = "Sasha_USER_BOT"
prefixies = ["."]

bot = Client(client_name, api_id=api_id, api_hash=api_hash)

def log_error(text: str):
    print(f"{Fore.LIGHTRED_EX}[ОШИБКА] {Fore.LIGHTCYAN_EX}{text}")

def log_text(text: str):
    print(f"{Fore.LIGHTGREEN_EX}[СООБЩЕНИЕ] {Fore.LIGHTCYAN_EX}{text}")

def error(text: str):
    return f"**❌ Ошибка**\n{text}"



def get_invis_text(message_text: str, last_text: str) -> str:
    text = ""

    for char in message_text:
        if char == " ":
            text += " "
            continue

        if random.randint(1, 4) != 1:
            text += f"||{char}||"
        else:
            text += char

    if text == last_text:
        return get_invis_text(message_text, text)
    else:
        return text


def get_boom_text(message_text: str, last_text: str) -> str:
    text = ""

    for char in message_text:
        if char == " ":
            text += " "
            continue

        if random.randint(1, 3) != 1:
            text += f"**{char.upper()}**"
        else:
            text += char

    if text == last_text:
        return get_boom_text(message_text, text)
    else:
        return text


async def get_user(text: Union[int, str]):
    async for dialog in bot.get_dialogs():
        if dialog.chat.first_name:
            if str(dialog.chat.id) == text:
                return int(text)

            name = dialog.chat.first_name if dialog.chat.last_name is None else f"{dialog.chat.first_name} {dialog.chat.last_name}"
            if text.lower() == name.lower():
                return dialog.chat.id
    return None


async def get_chat(text: Union[int, str]):
    async for dialog in bot.get_dialogs():
        if dialog.chat.title:
            if str(dialog.chat.id) == text:
                return int(text)

            title = dialog.chat.title
            if text.lower() == title.lower():
                return dialog.chat.id
    return None


async def get_dialog(text: Union[int, str]):
    async for dialog in bot.get_dialogs():
        if dialog.chat.first_name:
            if str(dialog.chat.id) == text:
                return int(text)

            name = dialog.chat.first_name if dialog.chat.last_name is None else f"{dialog.chat.first_name} {dialog.chat.last_name}"
            if text.lower() == name.lower():
                return dialog.chat.id
        else:
            if str(dialog.chat.id) == text:
                return int(text)

            title = dialog.chat.title
            if text.lower() == title.lower():
                return dialog.chat.id
    return None



async def task():
    while True:
        chat_actions: dict = json.loads((await execute("SELECT chat_actions FROM main")).fetchone()[0])
        for dialog_id in chat_actions:
            chat_action = chat_actions[dialog_id]

            if chat_action == "typing":
                await bot.send_chat_action(int(dialog_id), enums.ChatAction.TYPING)
            elif chat_action == "playing":
                await bot.send_chat_action(int(dialog_id), enums.ChatAction.PLAYING)
            elif chat_action == "video":
                await bot.send_chat_action(int(dialog_id), enums.ChatAction.RECORD_VIDEO)
            elif chat_action == "audio":
                await bot.send_chat_action(int(dialog_id), enums.ChatAction.RECORD_AUDIO)
            elif chat_action == "sticker":
                await bot.send_chat_action(int(dialog_id), enums.ChatAction.CHOOSE_STICKER)

        await asyncio.sleep(1)

async def on_ready():
    while not bot.is_connected:
        await asyncio.sleep(1)

    log_text("ЮзерБот успешно запущен!")
    await execute("CREATE TABLE IF NOT EXISTS main (lock_status BOOL, send_effect TEXT, auto_reactions TEXT, chat_actions TEXT)")

    if (await execute("SELECT * FROM main")).fetchone() is None:
        await execute(f"INSERT INTO main VALUES (?, ?, ?, ?)", [False, "default", json.dumps({}), json.dumps({})])

    await asyncio.create_task(task())


async def execute(sql: str, data: list = None):
    with sqlite3.connect("user_bot.sql") as connection:
        cursor = connection.cursor()

        async with asyncio.Lock():
            if data is not None:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

    return cursor

async def text_effect(message: types.Message):
    global screamers
    send_effect = (await execute("SELECT send_effect FROM main")).fetchone()[0]

    if send_effect == "print":
        cursor = "▌"

        if len(message.text) <= 10:
            cursor_size = 1
        elif len(message.text) <= 20:
            cursor_size = 2
        elif len(message.text) <= 50:
            cursor_size = 3
        elif len(message.text) <= 100:
            cursor_size = 4
        else:
            return

        message_text = message.text
        text = ""
        chars = message.text

        while text != message_text:
            await message.edit(text=text + cursor)

            if cursor_size == 1:
                await message.edit(text=text + chars[0])
                text += chars[0]
                chars = chars[1:]
            elif cursor_size == 2:
                if len(chars) >= 2:
                    await message.edit(text=text + chars[0:2])
                    text += chars[0:2]
                    chars = chars[2:]
                else:
                    await message.edit(text=text + chars[0])
                    text += chars[0]
                    chars = chars[1:]
            elif cursor_size == 3:
                if len(chars) >= 3:
                    await message.edit(text=text + chars[0:3])
                    text += chars[0:3]
                    chars = chars[3:]
                elif len(chars) >= 2:
                    await message.edit(text=text + chars[0:2])
                    text += chars[0:2]
                    chars = chars[2:]
                else:
                    await message.edit(text=text + chars[0])
                    text += chars[0]
                    chars = chars[1:]
            elif cursor_size == 4:
                if len(chars) >= 4:
                    await message.edit(text=text + chars[0:4])
                    text += chars[0:4]
                    chars = chars[4:]
                elif len(chars) >= 3:
                    await message.edit(text=text + chars[0:3])
                    text += chars[0:3]
                    chars = chars[3:]
                elif len(chars) >= 2:
                    await message.edit(text=text + chars[0:2])
                    text += chars[0:2]
                    chars = chars[2:]
                else:
                    await message.edit(text=text + chars[0])
                    text += chars[0]
                    chars = chars[1:]
    elif send_effect == "invis":
        text = message.text

        for i in range(7):
            text = get_invis_text(message.text, text)
            await message.edit(text)

        if message.text != text:
            await message.edit(message.text)
    elif send_effect == "boom":
        text = message.text

        for i in range(7):
            text = get_boom_text(message.text, text)
            await message.edit(text)

        if message.text != text:
            await message.edit(message.text)
    elif send_effect == "screamer":
        if screamers > 10:
            return

        screamers += 1

        for i in range(10):
            await asyncio.sleep(random.randint(5, 10))
            await message.edit("😈")
            await message.edit(message.text)

        screamers -= 1



@bot.on_message(filters.command(commands=["send_effect"], prefixes=prefixies))
async def _send_effect(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        send_effect = message.text.split()[1]
        await message.edit(f"{message.text}\n\n✅ **Успешно**\n\n🗑️ Сообщение будет удалено через минуту",
                           parse_mode=enums.ParseMode.MARKDOWN)
        await execute("UPDATE main SET send_effect = ?", [send_effect])

        await asyncio.sleep(60)
        await message.delete()


@bot.on_message(filters.command(commands=["lock"], prefixes=prefixies))
async def _lock(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        await message.edit(f"{message.text}\n\n✅ **Успешно**\n\n🗑️ Сообщение будет удалено через минуту",
                           parse_mode=enums.ParseMode.MARKDOWN)
        await execute("UPDATE main SET lock_status = ?", [True])

        await asyncio.sleep(60)
        await message.delete()


@bot.on_message(filters.command(commands=["unlock"], prefixes=prefixies))
async def _unlock(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        if message.text.lower().split()[1] == "321162":
            await message.edit(f"{message.text.split()[0]} ######\n\n✅ **Успешно**\n\n🗑️ Сообщение будет удалено через минуту",
                               parse_mode=enums.ParseMode.MARKDOWN)
            await execute("UPDATE main SET lock_status = ?", [False])
        else:
            passw = ""
            for char in message.text.split()[1]:
                passw += "#"

            await message.edit(f"{message.text.split()[0]} {passw}\n\n{error('Неверный код')}\n\n🗑️ Сообщение будет удалено через минуту",
                               parse_mode=enums.ParseMode.MARKDOWN)

        await asyncio.sleep(60)
        await message.delete()


@bot.on_message(filters.command(commands=["send"], prefixes=prefixies))
async def _send(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        arg = message.text.lower().split()[1]
        if arg == "dice":
            await bot.send_dice(message.chat.id)
        elif arg == "dart":
            await bot.send_dice(message.chat.id, "🎯")
        elif arg == "bowling":
            await bot.send_dice(message.chat.id, "🎳")
        elif arg == "basketball":
            await bot.send_dice(message.chat.id, "🏀")
        elif arg == "football":
            await bot.send_dice(message.chat.id, "⚽")

        await message.delete()



@bot.on_message(filters.command(commands=["auto_react"], prefixes=prefixies))
async def _auto_react(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        args_text = " ".join(message.text.split()[1:])
        args = args_text.split(",")

        i = 0
        for arg in args:
            args[i] = arg.strip()
            i += 1

        action = args[0].lower()
        await message.edit(f"{message.text}\n\n⌛ Поиск пользователя...")
        user_id = await get_user(args[1])

        if user_id is None:
            await message.edit(f"{message.text}\n\n{error('Указанный пользователь не найден!')}\n\n🗑️ Сообщение будет удалено через минуту",
                               parse_mode=enums.ParseMode.MARKDOWN)
            await asyncio.sleep(60)
            await message.delete()
            return

        auto_reactions: dict = json.loads((await execute("SELECT auto_reactions FROM main")).fetchone()[0])

        if action == "add":
            reaction = args[2]

            if str(user_id) in auto_reactions.keys():
                text = f"Для указанного пользователя добавлена автореакция!\nЕсли вы хотите изменить автореакцию для него, то сначала удалите её."
                await message.edit(f"{message.text}\n\n{error(text)}\n\n🗑️ Сообщение будет удалено через минуту",
                                   parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(60)
                await message.delete()
                return

            try:
                await message.react(reaction)
            except:
                text = "Вы неверно указали реакцию!\nУказанная реакция не поддерживается в telegram."
                await message.edit(f"{message.text}\n\n{error(text)}\n\n🗑️ Сообщение будет удалено через минуту",
                                   parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(60)
                await message.delete()
                return

            auto_reactions[str(user_id)] = reaction
        elif action == "remove":
            if str(user_id) not in auto_reactions.keys():
                await message.edit(f"{message.text}\n\n{error('Для указанного пользователя не добавлена автореакция!')}\n\n🗑️ Сообщение будет удалено через минуту",
                                   parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(60)
                await message.delete()
                return

            auto_reactions.pop(str(user_id))

        await message.edit(f"{message.text}\n\n✅ **Успешно**\n\n🗑️ Сообщение будет удалено через минуту",
                           parse_mode=enums.ParseMode.MARKDOWN)
        await execute("UPDATE main SET auto_reactions = ?", [json.dumps(auto_reactions)])
        await asyncio.sleep(60)
        await message.delete()



@bot.on_message(filters.command(commands=["chat_action"], prefixes=prefixies))
async def _chat_action(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        args_text = " ".join(message.text.split()[1:])
        args = args_text.split(",")

        i = 0
        for arg in args:
            args[i] = arg.strip()
            i += 1

        action = args[0]
        await message.edit(f"{message.text}\n\n⌛ Поиск диалога...")
        dialog_id = await get_dialog(args[1])

        if dialog_id is None:
            await message.edit(f"{message.text}\n\n{error('Указанный диалог не найден!')}\n\n🗑️ Сообщение будет удалено через минуту",
                               parse_mode=enums.ParseMode.MARKDOWN)
            await asyncio.sleep(60)
            await message.delete()
            return

        chat_actions: dict = json.loads((await execute("SELECT chat_actions FROM main")).fetchone()[0])

        if action == "add":
            chat_action = args[2].lower()

            if chat_action not in ["typing", "playing", "video", "audio", "sticker"]:
                await message.edit(f"{message.text}\n\n{error('Вы указали неверное действие диалог!')}\n\n🗑️ Сообщение будет удалено через минуту",
                                   parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(60)
                await message.delete()
                return

            if str(dialog_id) in chat_actions.keys():
                text = "В указанном диалоге выполняется действие!\nЕсли вы хотите изменить действие для него, то сначала удалите его."
                await message.edit(f"{message.text}\n\n{error(text)}\n\n🗑️ Сообщение будет удалено через минуту",
                                   parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(60)
                await message.delete()
                return

            chat_actions[str(dialog_id)] = chat_action
        elif action == "remove":
            if str(dialog_id) not in chat_actions.keys():
                await message.edit(f"{message.text}\n\n{error('В указанном диалоге не выполняется действие!')}\n\n🗑️ Сообщение будет удалено через минуту",
                                   parse_mode=enums.ParseMode.MARKDOWN)
                await asyncio.sleep(60)
                await message.delete()
                return

            chat_actions.pop(str(dialog_id))

        await message.edit(f"{message.text}\n\n✅ **Успешно**\n\n🗑️ Сообщение будет удалено через минуту",
                           parse_mode=enums.ParseMode.MARKDOWN)
        await execute("UPDATE main SET chat_actions = ?", [json.dumps(chat_actions)])
        await asyncio.sleep(60)
        await message.delete()

@bot.on_message(filters.command(commands=["info"], prefixes=prefixies))
async def _info(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        await message.edit(f"{message.text}\n\n⌛ Получаю и обрабатываю информацию...")

        auto_reactions: dict = json.loads((await execute("SELECT auto_reactions FROM main")).fetchone()[0])
        chat_actions: dict = json.loads((await execute("SELECT chat_actions FROM main")).fetchone()[0])
        isLock: bool = (await execute("SELECT lock_status FROM main")).fetchone()[0]
        send_effect = (await execute("SELECT send_effect FROM main")).fetchone()[0]

        auto_reactions_text = "**Автореакции**\n"
        for item in auto_reactions:
            reaction = auto_reactions.get(item)

            try:
                async for dialog in bot.get_dialogs():
                    if dialog.chat.first_name:
                        if dialog.chat.id == int(item):
                            user = dialog.chat
                            continue
            except:
                continue

            format_user = f"{user.first_name} (@{user.username})" if user.username else f"{user.first_name}"
            auto_reactions_text += f"{format_user} - {reaction}\n"

        chat_actions_text = "**Действия диалогов**\n"
        for item in chat_actions:
            chat_action = chat_actions.get(item)

            try:
                dialog = await bot.get_chat(item)
            except:
                continue

            chat_actions_text += f"{dialog.title if dialog.title else dialog.first_name} - {chat_action}\n"

        if send_effect not in ["boom", "invis", "print", "screamer"]:
            send_effect = "default"

        options = f"**Эффект написания сообщений:** {send_effect}\n**Блокировка отправки сообщений:** {'✅ активна' if isLock else '❌ неактивна'}"
        await message.edit(f"{message.text}\n\n{auto_reactions_text}\n{chat_actions_text}\n{options}",
                           parse_mode=enums.ParseMode.MARKDOWN)


@bot.on_message(filters.command(commands=["help"], prefixes=prefixies))
async def _help(client: Client, message: types.Message):
    if message.from_user.id == my_id:
        text = ("**Список команд**\n"
                "☛ **!send_effect** [ print | boom | invis | screamer ] - __установить эффект написания сообщений__\n"
                "☛ **!lock** - __заблокировать отправку сообщений__\n"
                "☛ **!unlock** [ код ] - __разблокировать отправку сообщений__\n"
                "☛ **!send** [ dice | dart | bowling | basketball | football ] - __быстро отправить анимированный стикер в чат__\n"
                "☛ **!auto_react** [ add | remove ], [ ID пользователя | Имя пользователя ], [ эмодзи для реакции ] - __управлять автореакциями__\n"
                "☛ **!chat_action** [ add | remove ], [ ID диалога | Имя диалога ], [ typing | playing | video | audio | sticker ] - __управлять действиями диалогов__\n"
                "☛ **!info** - __получить информацию о юзерботе__\n"
                "☛ **!help** - __получить список команд__\n")

        await message.edit(f"{message.text}\n\n{text}",
                           parse_mode=enums.ParseMode.MARKDOWN)



@bot.on_message()
async def on_message(client: Client, message: types.Message):
    if message.from_user:
        auto_reactions: dict = json.loads((await execute("SELECT auto_reactions FROM main")).fetchone()[0])

        if auto_reactions.get(str(message.from_user.id)) is not None:
            await message.react(auto_reactions.get(str(message.from_user.id)))

        if message.from_user.id == my_id:
            lock_status = (await execute("SELECT lock_status FROM main")).fetchone()[0]
            if lock_status:
                msg = await message.forward(main_chat_id)
                await message.delete()
                msg2 = await msg.reply(f"Сообщение не было доставлено в **{message.chat.title if message.chat.title is not None else message.chat.username}**, так как действует блокировка!\n\n🗑️ Сообщение будет удалено через минуту")
                await asyncio.sleep(60)

                try:
                    await msg.delete()
                except:
                    pass

                await msg2.delete()
            else:
                await text_effect(message)
    else:
        if message.chat.id == auto_send_comment_chat_id:
            gif_path = f"gifs/{random.randint(1, len(os.listdir('gifs')))}.gif"
            await message.reply_video(video=open(gif_path, "rb"))




loop = asyncio.new_event_loop()
Thread(target=lambda: loop.run_until_complete(on_ready())).start()

try:
    loop.run_until_complete(bot.run())
except unauthorized_401.AuthKeyUnregistered:
    log_error(f"Ключ не авторизован, удалите файл {client_name}.session и перезапустите программу!")
except unauthorized_401.AuthKeyInvalid:
    log_error("Вы указали неверный ключ!")
except unauthorized_401.SessionExpired:
    log_error(f"Сессия устарела, удалите файл {client_name}.session и перезапустите программу!")
except unauthorized_401.Unauthorized:
    log_error(f"Вы не авторизованы!")

