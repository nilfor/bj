from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton(text='馃挮袛芯斜邪胁懈褌褜 褌芯泻械薪馃挮'))
start_keyboard.add(KeyboardButton(text='馃寪 袛芯斜邪胁懈褌褜 薪械褋泻芯谢褜泻芯 褌芯泻械薪芯胁馃寪'))
start_keyboard.add(KeyboardButton(text='馃敯袠薪褎芯褉屑邪褑懈褟馃敯'), KeyboardButton(text='馃搳小褌邪褌懈褋褌懈泻邪馃搳'))
start_keyboard.add(KeyboardButton(text='馃摜校泻邪蟹邪褌褜 褉械泻胁懈蟹懈褌褘馃摜'))

props = InlineKeyboardMarkup()
props.add(InlineKeyboardButton(text='馃彽袙胁械褋褌懈 褉械泻胁懈蟹懈褌褘馃彽', callback_data='props'))

check_payment = ReplyKeyboardMarkup(resize_keyboard=True)
check_payment.add(KeyboardButton(text='袩褉芯胁械褉懈褌褜 芯锌谢邪褌褍'))
check_payment.add(KeyboardButton(text='袨褌屑械薪邪'))

admin = ReplyKeyboardMarkup(resize_keyboard=True)
admin.add(KeyboardButton(text='袟邪斜褉邪褌褜 写芯褋褌褍锌'))
admin.add(KeyboardButton(text='袙褘写邪褌褜 写芯褋褌褍锌'))
