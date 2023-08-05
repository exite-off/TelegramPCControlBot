import telebot
import time
import pyautogui
import win32api
from win32con import *
import keyboard as kb
import os

# initialize bot class
bot = telebot.TeleBot('YOUR TOKEN HERE')

# define authorized user ids
whitelist = [YOUR USERID HERE]

# define main keyboard layout
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('🔈 Volume Down', '🔊 Volume Up', '📷 Screenshot')
keyboard.row('⬆️ Scroll Up', '⬇️ Scroll Down', '⏯ Media control')

# media control keyboard layout
media_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
media_keyboard.row('⏮️ Previous', '⏯ Play/Stop', '⏭ Next')
media_keyboard.row('🔇 Mute/Unmute', '🏠 Main Menu')


def volume_up():
    kb.send('volume up')
    kb.send('volume up')
    kb.send('volume up')


def volume_down():
    kb.send('volume down')
    kb.send('volume down')
    kb.send('volume down')


def screenshot(message):
    image = pyautogui.screenshot()
    chat_id = message.chat.id
    image.save('screenshot.png')
    with open('screenshot.png', 'rb') as photo:
        bot.send_photo(chat_id, photo)
    os.remove('screenshot.png')


# define button handler function
def button_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in whitelist:
        if message.text == '🔊 Volume Up':
            volume_up()
            bot.send_message(chat_id, 'Volume up!')
        elif message.text == '🔈 Volume Down':
            volume_down()
            bot.send_message(chat_id, "Volume down!")
        elif message.text == '⬆️ Scroll Up':
            pyautogui.scroll(200)
            bot.send_message(chat_id, 'Scrolling up!')
        elif message.text == '📷 Screenshot':
            screenshot(message)
            bot.send_message(chat_id, 'Screenshot taken!')
            time.sleep(0.5)
        elif message.text == '⬇️ Scroll Down':
            pyautogui.scroll(-200)
            bot.send_message(chat_id, 'Scrolling down!')
        elif message.text == '⏯ Media control':
            bot.send_message(chat_id, 'Media Menu opened!', reply_markup=media_keyboard)
        elif message.text == '⏯ Play/Stop':
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
            bot.send_message(chat_id, 'Media playback toggled!')
        elif message.text == '⏭ Next':
            win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0xB0, KEYEVENTF_EXTENDEDKEY, 0)
            bot.send_message(chat_id, 'Next media is starting!')
        elif message.text == '⏮️ Previous':
            win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0xB1, KEYEVENTF_EXTENDEDKEY, 0)
            bot.send_message(chat_id, 'Previous media is starting!')
        elif message.text == '🔇 Mute/Unmute':
            kb.send("volume mute")
            bot.send_message(chat_id, 'Mute toggled successfully!')
        elif message.text == '🏠 Main Menu':
            bot.send_message(chat_id, 'Main Menu opened!', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'You are not authorized to use this bot.')


# handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I am exite's personal computer assistant. What can I do for you?", reply_markup=keyboard)


# handler for button press
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    button_handler(message)


# start the bot
bot.polling()
