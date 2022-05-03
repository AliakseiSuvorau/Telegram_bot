from bs4 import BeautifulSoup  # for scrapping the information
import requests  # for sending requests and getting html
from random import random
from time import sleep
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

# Now the bot itself
updater = Updater("5379448024:AAEfgCOeamwrNIkzuch4knAn33qMpzSyU8o", use_context=True)


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Type /find [body of the request]")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry, I don't understand you. Please, try /help")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Unknown command. Please, try /help")


user_request = ""


def find_ans(update: Update, context: CallbackContext):
    global user_request
    global answer_text
    user_request = " ".join(context.args)
    work_with_so(user_request)
    update.message.reply_text(answer_text)
    answer_text = ""


updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('find', find_ans))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


updater.start_polling()


url = "https://stackoverflow.com/questions"
answer_text = ""


def work_with_so(user_request):
    global answer_text
    if user_request == "":
        answer_text = "Please, enter the request"
        return
    questions = []
    cur_page = 1
    pages = 20

    while cur_page <= pages:
        url = "https://stackoverflow.com/questions" + "?tab=votes" + "&page=" + str(cur_page)
        response = requests.get(url)  # getting request from the site with the html
        html = BeautifulSoup(response.text, 'html.parser')
        question_data = html.find_all('div', class_="s-post-summary js-post-summary")
        if question_data:
            questions.extend(question_data)
            some_ms = random()
            sleep(some_ms)
        else:
            # print("No questions on English Stack Overflow")
            break
        cur_page += 1

    score = []
    href = []

    for item in questions:
        if len(score) < 5:
            if item.find('a', {"class": "s-link"}).text.lower().find(user_request.lower()) != -1:  # If the title suits the request
                if not (item.find('div', {"class": "s-post-summary--stats-item has-answers has-accepted-answer"}) is None):  # If there is a good answer
                    score.append(int(item.find('span', {"class": "s-post-summary--stats-item-number"}).text))
                    href.append("https://stackoverflow.com" + item.a.get('href'))
        else:
            break

    # print(f"Hits found on English Stack Overflow: {len(score)}")
    if len(score):
        answer_text += "Most relevant hits found on English Stack Overflow:\n"
    num_of_results = 5
    i = 0
    while i < min(num_of_results, len(score) + i):
        # print(f"Votes: {score[score.index(max(score), 0)]} ---->\t{href[score.index(max(score), 0)]}")
        answer_text = answer_text + "Votes: " + str(score[score.index(max(score), 0)]) + " ---->\t" + str(href[score.index(max(score), 0)]) + "\n"
        href.pop(score.index(max(score), 0))
        score.pop(score.index(max(score), 0))
        i += 1


    questions = []
    cur_page = 1


    while cur_page <= pages:
        url = "https://ru.stackoverflow.com/questions" + "?tab=votes" + "&page=" + str(cur_page)
        response = requests.get(url)  # getting request from the site with the html
        html = BeautifulSoup(response.text, 'html.parser')
        question_data = html.find_all('div', class_="s-post-summary js-post-summary")
        if question_data:
            questions.extend(question_data)
            some_ms = random()
            sleep(some_ms)
        else:
            # print("No questions on Russian Stack Overflow")
            break
        cur_page += 1


    score = []
    href = []

    for item in questions:
        if len(score) < 5:
            if item.find('a', {"class": "s-link"}).text.lower().find(user_request.lower()) != -1:  # If the title suits the request
                if not (item.find('div', {"class": "s-post-summary--stats-item has-answers has-accepted-answer"}) is None):  # If there is a good answer
                    score.append(int(item.find('span', {"class": "s-post-summary--stats-item-number"}).text))
                    href.append("https://ru.stackoverflow.com" + item.a.get('href'))
        else:
            break


    # This part of code finds ALL of most voted answers
    # start = 0
    # try:
    #     while True:
    #         i = score.index(max(score), start)
    #         print(score[i], href[i], sep='\t')
    #         answer_url = href[i]
    #         answer_response = requests.get(answer_url)
    #         answer_html = BeautifulSoup(answer_response.text, 'html.parser')
    #         start = score.index(max(score), start + 1)
    # except ValueError:
    #     pass

    if len(score):
        answer_text += "Most relevant hits found on Russian Stack Overflow:\n"
    # print(f"Hits found on Russian Stack Overflow: {len(score)}")
    num_of_results = 5
    i = 0
    while i < min(num_of_results, len(score) + i):
        # print(f"Votes: {score[score.index(max(score), 0)]} ---->\t{href[score.index(max(score), 0)]}")
        answer_text = answer_text + "Votes: " + str(score[score.index(max(score), 0)]) + " ---->\t" + str(href[score.index(max(score), 0)]) + "\n"
        href.pop(score.index(max(score), 0))
        score.pop(score.index(max(score), 0))
        i += 1
