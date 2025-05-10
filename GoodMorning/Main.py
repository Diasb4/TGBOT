import requests
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import random
import logging
import os
import subprocess
import sys
from telethon import TelegramClient, errors

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Конфигурация клиента Telegram
api_id = 24220695
api_hash = 'bc95f67d8d33e2b342075ef793c0ed8b'
phone = '+77085083767'
username = 'Not404Dias'
session_file = '/GoodMorning/Not404Dias.session'

# Настройки API OpenWeatherMap
api_key = "5fc94082b0bd5d73c10e14c959ac190a"  # Замени на свой новый API-ключ
city = "Astana"
weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}&lang=ru"

# Минимальные компоненты для генерации утренних сообщений
morning_greetings = ["Доброе утро", "С добрым утром", "Утро доброе"]
morning_wishes = ["успехов", "бодрости", "радости", "энергии"]
morning_extras = ["сегодня", "на день", "с утра"]

# Минимальные компоненты для генерации ночных сообщений
night_greetings = ["Спокойной ночи", "Доброй ночи", "Тихой ночи"]
night_wishes = ["сладких снов", "хорошего отдыха", "крепкого сна"]
night_extras = ["на ночь", "до утра", "в тишине"]

# Списки эмодзи для утренних и ночных сообщений
morning_emojis = [
    "٩(◕‿◕｡)۶", "<(￣︶￣)>", "(＠＾◡＾)", "(≧◡≦)", "＼(￣▽￣)／", "╰(*´︶`*)╯", "(◠‿◕)", "ฅ^•ﻌ•^ฅ",
    "ʘ‿ʘ", "(θ‿θ)", "ʘ‿ʘ", "(◔‿◔)", "(ʘᴗʘ✿)", "(ʘᴗʘ✿)", "(. ❛ ᴗ ❛.)", "(≧▽≦)",
    "(◕ᴗ◕✿)", "( ╹▽╹ )", "(☆▽☆)", "(◍•ᴗ•◍)", "<(￣︶￣)>", "(✿^‿^)", "(◡ ω ◡)",
    "(｡•̀ᴗ-)✧", "( ꈍᴗꈍ)", "( ´◡‿ゝ◡`)"
]
night_emojis = [
    "٩(◕‿◕｡)۶", "<(￣︶￣)>", "(＠＾◡＾)", "(≧◡≦)", "＼(￣▽￣)／", "╰(*´︶`*)╯", "(◠‿◕)", "ฅ^•ﻌ•^ฅ",
    "ʘ‿ʘ", "(θ‿θ)", "ʘ‿ʘ", "(◔‿◔)", "(ʘᴗʘ✿)", "(ʘᴗʘ✿)", "(. ❛ ᴗ ❛.)", "(≧▽≦)",
    "(◕ᴗ◕✿)", "( ╹▽╹ )", "(☆▽☆)", "(◍•ᴗ•◍)", "<(￣︶￣)>", "(✿^‿^)", "(◡ ω ◡)",
    "(｡•̀ᴗ-)✧", "( ꈍᴗꈍ)", "( ´◡‿ゝ◡`)"
]

# Списки пользователей и ключевых слов для Доброго утра и Спокойной ночи
users_and_messages_good_morning = [
    {'user_id': -1001293963473, 'key': 'склад мемов с нижнего интернета'},
    {'user_id': -1002250858069, 'key': 'перваши'},
    {'user_id': -1002331611327, 'key': 'Сешники дорогие'},
    {'user_id': -1002231527911, 'key': 'группа'},
    {'user_id': -1001997403257, 'key': 'ремудлики'},
    {'user_id': -1001909414801, 'key': 'искатели приключений'},
    # {'user_id': -1001611321057, 'key': 'волонтерыши'},
    {'user_id': -1002442667162, 'key': 'амбасадорики флуд'},
    # {'user_id': -1002450991590, 'key': 'амбасадоры'},
    {'user_id': -1001406990587, 'key': 'Геймеры'},
    # {'user_id': -1002272005326, 'key': 'чивапчичи'},
    # {'user_id': -1002459163538, 'key': '4 поток'},
    {'user_id': -1002147993797, 'key': 'канал'},
    {'user_id': -1002203836183, 'key': 'Спортики'},
    {'user_id': -1002311901510, 'key': 'Рири и ее подписота'},
    {'user_id': -1001760986011, 'key': 'Аноны'},
    {'user_id': -1001977582154, 'key': 'Мегамайнды'},
    {'user_id': -1001446142829, 'key': 'Стафф Гениев'},
    {'user_id': 769050344, 'key': 'Кали'},
]

users_and_messages_good_night = [
    # {'user_id': -1001883621101, 'key': 'Аскар'},
    # {'user_id': -1001883621101, 'key': 'Амангельды'},
    # {'user_id': -1001883621101, 'key': 'Рири'},
    # {'user_id': -1001883621101, 'key': 'Игнис'},
    # {'user_id': -1001883621101, 'key': 'Руру'},
    # {'user_id': -1001883621101, 'key': 'Алих'},
    # {'user_id': -1001883621101, 'key': 'Асем-босс'},
    # {'user_id': -1001883621101, 'key': 'Асем'},
    # {'user_id': -1001883621101, 'key': 'пустой ник'},
    # {'user_id': -1001883621101, 'key': 'Гукка'},
    # {'user_id': -1001883621101, 'key': 'Дани'},
    # {'user_id': -1001883621101, 'key': 'Кпв'},
    # {'user_id': -1001883621101, 'key': 'те кого я не могу вспомнить'},
    # {'user_id': -1001883621101, 'key': 'кнб'},
    # {'user_id': -1001883621101, 'key': 'всем'},
    {'user_id': -1001293963473, 'key': 'склад мемов с нижнего интернета'},
    {'user_id': -1002250858069, 'key': 'перваши'},
    {'user_id': -1002331611327, 'key': 'Сешники дорогие'},
    {'user_id': -1002231527911, 'key': 'группа'},
    {'user_id': -1001997403257, 'key': 'ремудлики'},
    {'user_id': -1001909414801, 'key': 'искатели приключений'},
    # {'user_id': -1001611321057, 'key': 'волонтерыши'},
    {'user_id': -1002442667162, 'key': 'амбасадорики флуд'},
    # {'user_id': -1002450991590, 'key': 'амбасадоры'},
    {'user_id': -1001406990587, 'key': 'Геймеры'},
    # {'user_id': -1002272005326, 'key': 'чивапчичи'},
    # {'user_id': -1002459163538, 'key': '4 поток'},
    {'user_id': -1002147993797, 'key': 'канал'},
    {'user_id': -1002203836183, 'key': 'Спортики'},
    {'user_id': -1002311901510, 'key': 'Рири и ее подписота'},
    {'user_id': -1001760986011, 'key': 'Аноны'},
    {'user_id': -1001977582154, 'key': 'Мегамайнды'},
    {'user_id': -1001446142829, 'key': 'Стафф Гениев'},
    {'user_id': 769050344, 'key': 'Кали'},
]

# Варианты синонимов
adventure_synonyms_morning = [
    "авантюристы", "искатели приключений", "путешественники", "сорвиголовы",
    "первооткрыватели", "странники"
]

adventure_synonyms_night = [
    "искатели приключений", "путешественники", "первооткрыватели", "странники"
]


# Функция для получения погоды на сегодня
def get_weather_today():
    try:
        response = requests.get(weather_url, timeout=10)
        data = response.json()

        # Проверяем код ответа
        if response.status_code != 200:
            raise Exception(f"API вернул ошибку: {data.get('message', 'Неизвестная ошибка')}")

        # Проверяем, есть ли ключ "list"
        if "list" not in data:
            raise KeyError(f"Ключ 'list' не найден в ответе API. Ответ: {data}")

        # Агрегируем данные по дням
        daily_temps = defaultdict(lambda: {"max": float("-inf"), "min": float("inf"), "temps": [], "weather": []})
        for entry in data["list"]:
            dt = datetime.fromtimestamp(entry["dt"])
            day_key = dt.strftime("%a %d")
            temp = entry["main"]["temp"]
            weather_desc = entry["weather"][0]["description"]  # Получаем описание погоды
            daily_temps[day_key]["temps"].append(temp)
            daily_temps[day_key]["max"] = max(daily_temps[day_key]["max"], temp)
            daily_temps[day_key]["min"] = min(daily_temps[day_key]["min"], temp)
            daily_temps[day_key]["weather"].append(weather_desc)

        # Берем погоду на сегодня (первый день)
        today = list(daily_temps.items())[0]
        day, temps = today
        max_temp = round(temps["max"])
        min_temp = round(temps["min"])

        # Определяем наиболее частое состояние погоды за день
        weather_conditions = temps["weather"]
        most_common_weather = max(set(weather_conditions), key=weather_conditions.count)

        return f"Погода в Астане на сегодня ({day}):  {max_temp}°/{min_temp}°, {most_common_weather}"
    except Exception as e:
        logging.error(f"Ошибка получения погоды: {e}")
        return None  # Возвращаем None вместо сообщения об ошибке


def generate_morning_message(key, include_weather=False):
    greeting = random.choice(morning_greetings)
    wish = random.choice(morning_wishes)
    extra = random.choice(morning_extras)
    emoji = random.choice(morning_emojis)
    if key == 'авантюристы':
        key = random.choice(adventure_synonyms_morning)

    message = f"{greeting}, {key}, {wish} {extra} {emoji}"
    if include_weather:
        weather = get_weather_today()
        if weather:  # Добавляем погоду только если она успешно получена
            message += f"\n{weather}"
    return message


def generate_night_message(key):
    greeting = random.choice(night_greetings)
    wish = random.choice(night_wishes)
    extra = random.choice(night_extras)
    emoji = random.choice(night_emojis)
    if key == 'искатели приключений':
        key = random.choice(adventure_synonyms_night)
    return f"{greeting}, {key}, {wish} {extra} {emoji}"


async def send_messages(client, messages_list, is_morning=False, batch_size=5):
    # Перемешиваем все сообщения
    random.shuffle(messages_list)

    sent_chats = set()
    last_chat_id = None

    # Чаты, в которые добавляем погоду
    weather_chats = {-1002331611327, -1002250858069}  # Сешники дорогие и перваши

    # Отправка сообщений из списка
    for i in range(0, len(messages_list), batch_size):
        batch = messages_list[i:i + batch_size]
        for item in batch:
            user_id = item['user_id']
            key = item['key']
            # Добавляем погоду только для Сешников и первашей
            include_weather = is_morning and user_id in weather_chats
            message = generate_morning_message(key, include_weather) if is_morning else generate_night_message(key)

            if user_id == last_chat_id:
                delay = random.uniform(20, 25)
            else:
                delay = random.uniform(30, 40)
            logging.info(f"Waiting {delay:.2f} seconds before sending to chat ID: {user_id}")
            await asyncio.sleep(delay)

            if not client.is_connected():
                logging.warning(f"Client disconnected. Attempting to reconnect to chat ID: {user_id}")
                for attempt in range(3):
                    try:
                        await client.connect()
                        if await client.is_user_authorized():
                            logging.info(f"Reconnected successfully to chat ID: {user_id}")
                            break
                    except Exception as e:
                        logging.error(f"Reconnection attempt {attempt + 1}/3 failed: {e}")
                        await asyncio.sleep(10)
                else:
                    logging.error(f"Failed to reconnect after 3 attempts for chat ID: {user_id}")
                    continue

            try:
                await client.send_message(user_id, message)
                logging.info(f"Message sent to chat with ID: {user_id}: {message}")
                sent_chats.add(user_id)
            except errors.FloodWaitError as e:
                logging.warning(f"Flood wait detected for {e.seconds} seconds. Pausing...")
                await asyncio.sleep(e.seconds + 5)
            except Exception as e:
                logging.error(f"Error while sending to chat ID {user_id}: {e}")
            last_chat_id = user_id
        if i + batch_size < len(messages_list):
            logging.info(f"Pausing 60 seconds before next batch...")
            await asyncio.sleep(60)

    message_type = "утренние" if is_morning else "ночные"
    logging.info(f"Все {message_type} сообщения отправлены.")

    if is_morning and os.name == 'nt':
        logging.info("Запуск команды выключения компьютера после утренних сообщений...")
        try:
            result = subprocess.run(
                ["shutdown", "/s", "/t", "10"],
                capture_output=True,
                text=True,
                check=True,
                timeout=15
            )
            logging.info(f"Компьютер будет выключен через 10 секунд. Вывод команды: {result.stdout}")
        except subprocess.TimeoutExpired as e:
            logging.error(f"Команда выключения превысила время ожидания: {e.stdout} {e.stderr}")
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Ошибка выполнения команды выключения: код {e.returncode}, вывод: {e.stdout}, ошибка: {e.stderr}")
        except Exception as e:
            logging.error(f"Неизвестная ошибка при выключении компьютера: {str(e)}")
    elif os.name == 'nt':
        try:
            result = subprocess.run(
                ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                capture_output=True,
                text=True,
                check=True,
                timeout=15
            )
            logging.info("После ночных сообщений компьютер переходит в спящий режим.")
        except Exception as e:
            logging.error(f"Ошибка при переходе в спящий режим: {e}")
    else:
        logging.info("Система не Windows, выключение не поддерживается.")


async def main():
    max_retries = 5
    retry_delay = 30
    connection_params = {'connection_retries': 10, 'timeout': 120}

    for attempt in range(max_retries):
        try:
            async with TelegramClient(session_file, api_id, api_hash, **connection_params) as client:
                # Автоматический ввод телефона
                await client.start(phone=lambda: "+77085083767")
                logging.info("Client successfully connected")

                logging.info(f"Received arguments: {sys.argv}")
                if len(sys.argv) > 1:
                    arg = sys.argv[1].lower().strip()
                    logging.info(f"Processed argument: {arg}")
                    if arg == 'morning':
                        logging.info("Manual launch of morning messages...")
                        await send_messages(client, users_and_messages_good_morning, is_morning=True)
                    elif arg == 'night':
                        logging.info("Manual launch of night messages...")
                        await send_messages(client, users_and_messages_good_night, is_morning=False)
                    else:
                        logging.warning(f"Unknown argument: {arg}. Exiting.")
                else:
                    logging.warning("Argument not specified. Use 'morning' or 'night' to launch.")
                break

        except (errors.FloodWaitError, errors.SessionPasswordNeededError, OSError, TimeoutError) as e:
            logging.error(f"Connection error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying connection in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logging.error("Exceeded maximum number of connection attempts. Exiting.")
                break
        finally:
            if 'client' in locals() and client.is_connected():
                await client.disconnect()
                logging.info("Client disconnected")


if __name__ == '__main__':
    asyncio.run(main())