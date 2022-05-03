import functions as f
import Globals as g
from telegram.update import Update
import telegram.ext as t


updater = t.Updater("5379448024:AAEfgCOeamwrNIkzuch4knAn33qMpzSyU8o", use_context=True)


# What to answer on "/help"
def help(update: Update, context: t.CallbackContext):
    update.message.reply_text("Type /find [body of the request]")


# What to answer on a message without "/"
def unknown_text(update: Update, context: t.CallbackContext):
    update.message.reply_text(
        "Sorry, I don't understand you. Please, try /help")


# What to answer on a message with "/", which doesn't match any command on the list
def unknown(update: Update, context: t.CallbackContext):
    update.message.reply_text(
        "Unknown command. Please, try /help")


# Create an answer on a request
def find_ans(update: Update, context: t.CallbackContext):
    g.user_request = " ".join(context.args)
    answer_text = f.work_with_so()
    update.message.reply_text(answer_text)


updater.dispatcher.add_handler(t.CommandHandler('help', help))
updater.dispatcher.add_handler(t.CommandHandler('find', find_ans))
updater.dispatcher.add_handler(t.MessageHandler(t.Filters.command, unknown))
updater.dispatcher.add_handler(t.MessageHandler(t.Filters.text, unknown_text))


# Start telegram bot
updater.start_polling()
