import telebot, json, os, time, datetime
from telebot import types, apihelper

PROXY_URL = "Прокси тоже не дам"
apihelper.proxy = {'http': PROXY_URL, 'https': PROXY_URL}
with open("assets/index.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    f.close()

with open("assets/acc.json", "r", encoding="utf-8") as f:
    acc = json.load(f)
    f.close()

api = telebot.TeleBot(data["token"])

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("✅ Проверить подписку")
    if message.from_user.id in acc["admin"]: markup.row("🗒 Перезапуск бота", "🖥 Команды")
    return markup

@api.message_handler(content_types=["text"])
def message(message):
    try:
        with open(f"chats/{message.from_user.id}.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.date.today()} | {datetime.datetime.now().hour}:{datetime.datetime.now().minute}] @{message.from_user.username} ({message.from_user.id}): {message.text}\n")
            f.close()
        if message.from_user.id in acc["banned"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            api.send_message(message.from_user.id, "❌ Извиняемся, но...\nВы были отправлены в чёрный список.", reply_markup=markup)
            pass
        else:
            if message.from_user.id in acc["admin"]:
                msg = message.text.split(" ")
                if msg[0] == "/say":
                    a = 0
                    while(1):
                        try:
                            if a == len(acc["users"]): break 
                            else:
                                api.send_message(acc["users"][a], f"{message.text[4:len(message.text)]}")
                                a += 1
                        except: a += 1
                elif msg[0] == "/ban":
                    try: 
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        acc["banned"].append(int(msg[1]))
                        with open(f'assets/acc.json', "w", encoding="utf-8") as f:
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp1['name']} был заблокирован!")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, которого хотели заблокировать не существует!")
                elif msg[0] == "/unban":
                    try: 
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        acc["banned"].remove(int(msg[1]))
                        with open(f'assets/acc.json', "w", encoding="utf-8") as f:
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp1['name']} был разблокирован!")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, которого хотели разблокировать не существует!")
                elif msg[0] == "/tgkon" and message.from_user.id in acc["admin"]:
                  try:
                      with open('assets/acc.json', "w", encoding="utf-8") as f:
                          acc["tgk"].append(msg[1])
                          json.dump(acc, f)
                          f.close()
                      api.send_message(message.from_user.id, f"✅ {msg[1]} добавлен в обязательные тгк, но попросите добавить админа этого тгк чтобы бот мог корректно работать!")
                  except: api.send_message(message.from_user.id, f"❌ Меня не добавили в {msg[1]}. Пожалуйста, добавьте в этот тгк")
                elif msg[0] == "/tgkoff" and message.from_user.id in acc["admin"]:
                    try:
                        with open('assets/acc.json', "w", encoding="utf-8") as f:
                            acc["tgk"].remove(msg[1])
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ {msg[1]} убран из обязательных тгк!")
                    except: api.send_message(message.from_user.id, f'❌ {msg[1]} не был в обязательных подписок')
                elif msg[0] == "/send":
                    t = message.text.split('"')
                    api.send_message(int(t[1]), t[3])
                    api.send_message(message.from_user.id, "✅ Отправлено!")
                else:
                    if message.text == "✅ Проверить подписку" or message.text == "/start": pass
                    elif message.text == "🗒 Перезапуск бота":
                        api.send_message(message.from_user.id, "✅ Бот перезапускается...")
                        os.system("python3 main.py")
                        exit(0)
                    elif message.text == "🖥 Команды":
                        api.send_message(message.from_user.id, "Команды:\n\n/say {текст} - отправка сообщения всем кто активировал бота\n/ban {id} - пермач (бан на всегда) для юзера\n/unban {id} - снять блокировку\n/tgkon @{юзернейм тгк} - добавить тгк в обязательные подписки\n/tgkoff @{юзернейм тгк} - убрать тгк из обязательных подписок\n/send \"{id}\" \"{текст}\" - отправить сообщение пользователю по id")
                    else: api.send_message(message.from_user.id, "❌ Неизвестная команда!")
            if message.text == "/start" or message.text.split(" ")[0] == "/start":
                if message.from_user.id not in acc["users"]:
                    acc["users"].append(message.from_user.id)
                    with open("assets/acc.json", "w", encoding="utf-8") as f:
                        json.dump(acc, f)
                        f.close()
                    a = f", @{message.from_user.username}"
                else:
                    a = f", @{message.from_user.username}"
                api.send_message(message.from_user.id, f"👋 Приветствую{a}!\n\nДанный бот предназначен для пропуска в чат Алисы.\nПрежде чем заходить, подпишитесь на <a href='https://sozvezdie_lisy.t.me/'>данный канал</a>, позже нажмите кнопку ниже.", reply_markup=main_menu(message=message), parse_mode="HTML")
            elif message.text == "✅ Проверить подписку":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                api.send_message(message.from_user.id, "⚙ Проверка подписки на обязательные тгк...", reply_markup=markup)
                tgk = []
                for i in range(0, len(acc["tgk"])):
                    temp = api.get_chat_member(acc["tgk"][i], message.from_user.id)
                    if temp.status != "left": tgk.append(1)
                    else: tgk.append(0)
                if tgk.count(0) == 0:
                    api.send_message(message.from_user.id, "✅ Вы подписаны на все обязательные тгк!\n\nСсылка на чат: https://t.me/+Nd7mX9zwL4Q3OTBi")
                else:
                    l = ""
                    markup = types.InlineKeyboardMarkup()
                    for i in range(0, tgk.count(0)):
                        l += f"{acc['tgk'][tgk.index(0)]}\n"
                        button1 = types.InlineKeyboardButton("Подписаться", url=f'https://{acc["tgk"][tgk.index(0)][1:len(acc["tgk"][tgk.index(0)])]}.t.me/')
                        markup.add(button1)
                        tgk[tgk.index(0)] = ""
                    api.send_message(message.from_user.id, f"❌ Вы не подписались на все тгк!\n\nПодпишитесь на:\n{l}\nПосле чего нажмите на кнопку ниже 'Проверить подписку'.", reply_markup=markup)
                pass
            else:
                if message.text in ["/tgkon", "/tgkoff", "/ban", "/unban", "/say", "/send"] and message.from_user.id in acc["admin"]: pass
                else: api.send_message(message.from_user.id, "❌ Неизвестная команда!")
    except Exception as e:
        api.send_message(1959168915, f"Произошла ошибка в коде.\n\nError: {e}\nMessage: {message.text}")
        api.send_message(message.from_user.id, f"Произошла ошибка в коде.\n\nError: {e}\nMessage: {message.text}") 
        with open("ex.txt", "a", encoding="utf-8") as file:
            file.write(f"Error: {e}\nMessage: {message.text}\n") 
            file.close()

@api.chat_join_request_handler()
def req_join(message):
    try:
        tgk = 0
        for i in range(0, len(acc["tgk"])):
            temp = api.get_chat_member(acc["tgk"][i], message.from_user.id)
            if temp.status != "left": pass
            else: tgk = 1
        if tgk == 0:
            api.approve_chat_join_request(message.chat.id, message.from_user.id)
            time.sleep(1)
            if message.from_user.username == None:
                hello = "Привет!"
            else: 
                hello = f"Привет, @{message.from_user.username}!"
            api.send_message(message.chat.id, f"{hello} <a href='https://t.me/c/3813344465/202'>Тут правила</a>", parse_mode="HTML")
            api.send_message(message.chat.id, "А так добро пожаловать 🩷")
        else: api.decline_chat_join_request(message.chat.id, message.from_user.id)
    except Exception as e:
        with open("ex.txt", "a", encoding="utf-8") as file:
            file.write(f"Error: {e}\nMessage: {message.text}\n") 
            file.close()

while(1):
    try:
        api.polling()
    except Exception as e:
        if str(e).count('Cannot connect to proxy.') == 1:
            print("Прокси временно лестница (не работает), перезапуск через 5 секунд")
        else:
            print(f"Неизвестная ошибка: {e}\nПерезапуск через 5 секунд")
        time.sleep(5)