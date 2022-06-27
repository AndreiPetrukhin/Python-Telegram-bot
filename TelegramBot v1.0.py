from telegram.ext import Updater
from telegram import ReplyKeyboardMarkup # Для создания клавиатуры
from datetime import datetime, timedelta, time
now = datetime.now()

updater = Updater(token='5365879922:AAE0c_4tkKTrZ3Aa23KMGbvjNDvkITkTe0o', use_context=True)

dispatcher = updater.dispatcher
job_queue = updater.job_queue #Для создания очереди задач (отправки сообщений еженедельно и ежедневно)

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

reply_keyboard = [['/How_it_works', '/How_to_use_this_bot'],
                  ['/Week_results', '/Imposter_syndrome_test']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать! Если вас заинтересовал данный бот, это означает, что вы как и 70% людей столкнулись с \"Синдромом Самозванца\". Просто знайте, что вы не одиноки и вместе мы постараемся уличшить ваше психоэмоциональное состояние.\n\nПожалуйста, ознакомьтесь с разделами меню /How_it_works и /How_to_use_this_bot.\nСпасибо и удачи!", reply_markup=markup)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def wp(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="️Концепция - проста❗️\n🔸Бот отправляет вам ежедневные напоминания\n🔹Вы ежедневно делитесь с ботом вашими результатами (рабочие задачи, успехи в хобби, благотворительные активности и т.п.)\n🔸Бот собирает и бережно хранит информацию\n🔸Бот отправляет вам еженедельный отчет о проделанной работе\n\nТаким образом, на еженедельной основе вы получаете подтверждение вашей результативности.", reply_markup=markup)
wp_handler = CommandHandler('How_it_works', wp)
dispatcher.add_handler(wp_handler)

def instruction(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="1️⃣ Одно сообщение = одна выполненая цель или активность\n2️⃣ Можете писать на любом языке и даже отправлять смайлики 😳 и эмодзи. Главное, что вы понимаете какое именно задание было выполнено\n3️⃣ Получить справку о еженедельных результатах можно в разделе меню /Week_results\n4️⃣ Пройти тест на наличие у вас Синдрома Самозванца можно в разделе меню /Imposter_syndrome_test", reply_markup=markup)
instruction_handler = CommandHandler('How_to_use_this_bot', instruction)
dispatcher.add_handler(instruction_handler)

def test(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Попробуйте пройти тест на наличие синдрома самозванца: https://testsonline.net/blog/psy/test-na-sindrom-samozvantsa/ \n\nПримечание: данный тест не является показанием к тому, что вы обладаете синдромом самозванца. Если вы хотите получить официальное заключение, пожаулйста, обратитесь к квалифицированному, практикующему специалисту.", reply_markup=markup)
test_handler = CommandHandler('Imposter_syndrome_test', test)
dispatcher.add_handler(test_handler)

from telegram.ext import MessageHandler, Filters
import requests
import json

def notion_import(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='"' + update.message.text + '" Successfully added to Notion')  # for text reverse use [::-1]
    with open('/Users/apetrukh/PythonHW/Telegram bot/Test_JSON_2.json', 'w') as ouf: # Путь для хоста /home/RonDron/Test_JSON_2.json
        ouf.write('{"parent": { "database_id": "b6c859f4bfb1420cbab9eff1d4e4baf1" },"properties": {"title": {"title": [{"text": {"content":"')
        ouf.write(update.message.text)
        ouf.write('"}}]},"User_ID": {"rich_text": [{"text": {"content": "')
        ouf.write(str(update.message['chat']['id']))
        ouf.write('"}}]}}}')

    API_ENDPOINT = "https://api.notion.com/v1/pages"
    HEADERS = {"Authorization": "Bearer secret_1CVYKDIr1KNRaiot49TwRM9TCsHnLWKWCpG53lC4XPr", "Content-Type": "application/json", "Notion-Version": "2021-08-16"}
    with open('/Users/apetrukh/PythonHW/Telegram bot/Test_JSON_2.json', 'r') as f: # Путь для хоста /home/RonDron/Test_JSON_2.json
        DATA = json.load(f)

    r = requests.post(API_ENDPOINT, data=json.dumps(DATA), headers=HEADERS)

notion_import_handler = MessageHandler(Filters.text & (~Filters.command), notion_import)
dispatcher.add_handler(notion_import_handler)

def notion_export(update: Update, context: CallbackContext):
    goals_result = ''
    user_id_notion = ''
    user_id_bot = ''
    count = 0
    API_ENDPOINT = f'https://api.notion.com/v1/databases/b6c859f4bfb1420cbab9eff1d4e4baf1/query'
    HEADERS = {"Authorization": "Bearer secret_1CVYKDIr1KNRaiot49TwRM9TCsHnLWKWCpG53lC4XPr", "Notion-Version": "2021-08-16"}

    r = requests.post(API_ENDPOINT, headers=HEADERS)
    result_dict = r.json()

    user_id_bot = str(update.message['chat']['id']) # присвоение переменной id пользователя из приложения телеграмм
    for i in range(len(result_dict['results'])):
        user_id_notion = result_dict['results'][i]['properties']['User_ID']['rich_text'][0]['text']['content'] # присвоение переменной id пользователя из Notion в формате str()
        record_date = result_dict['results'][i]['properties']['Goal_completion_date']['created_time'] # присваеваем переменной дату создания записи в Notion
        record_date = datetime.strptime(record_date[0:len(record_date) - 1], '%Y-%m-%dT%H:%M:%S.%f') # переводим дату из Notion в формат YYYY-MM-DD HH:MM:SS:ffff удаляя последний символ Z
        if user_id_notion == user_id_bot and record_date >= now - timedelta(days=7):
            count += 1
            goals_result = goals_result + str(count) + '. ' + result_dict['results'][i]['properties']['Name']['title'][0]['text']['content'] + '\n'
    goals_result = goals_result + '\nЗа последнюю неделю вы выполнили ' + str(count) + ' задач! Отлично, Вы большой молодец:)'
    context.bot.send_message(chat_id=update.effective_chat.id, text=goals_result, reply_markup=markup)

notion_export_handler = CommandHandler('Week_results', notion_export)
dispatcher.add_handler(notion_export_handler)

def callback_day(context: CallbackContext):
    id_base = []
    API_ENDPOINT = f'https://api.notion.com/v1/databases/b6c859f4bfb1420cbab9eff1d4e4baf1/query'
    HEADERS = {"Authorization": "Bearer secret_1CVYKDIr1KNRaiot49TwRM9TCsHnLWKWCpG53lC4XPr",
               "Notion-Version": "2021-08-16"}

    r = requests.post(API_ENDPOINT, headers=HEADERS)
    result_dict = r.json()

    for i in range(len(result_dict['results'])):
        user_id_notion = result_dict['results'][i]['properties']['User_ID']['rich_text'][0]['text']['content']
        if user_id_notion not in id_base:
            id_base += [user_id_notion]
    for i in range(len(id_base)):
        context.bot.send_message(chat_id=id_base[i], text='Здравствуйте, предлагаю вам поделиться со мной своими результатами за день. Это могут быть задачи, активности и т.п., за которые вы можете себя похвалить. Например: провел утреннюю медитацию, сходил в спортивный зал, помог родителям, завершил обучение.', reply_markup=markup)

job_day = job_queue.run_daily(callback_day, time.fromisoformat('18:00:00'))

# def caps(update: Update, context: CallbackContext): #CAPS function for the text
#    text_caps = ' '.join(context.args).upper()
#    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# caps_handler = CommandHandler(caps)
# dispatcher.add_handler(caps_handler)

updater.start_polling()
updater.idle() # Для корректной работы job_queue