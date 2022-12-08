import time;
import handleAPI;
from telegram.ext import *
from telegram import *
import constants;
from datetime import date;
import threading;
import os;
from requests import *;
import traceback;
import handleData;


#convert data to list
def Convert(data):
    datanew = data.strip("[]").split(', ')
    return datanew;

d2 = 7;
def t_updatelistCoins():
    while 1>0:
        d1 =date.today();
        thisDay = d1.strftime("%d");
        if(int(thisDay)!=d2):
            handleAPI.getListCoins();
            time.sleep(14400);

updater = Updater(token="5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w");
dispatcher = updater.dispatcher;

def startCommand(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to crypto hunter");
    t1 = threading.Thread(target=handleData.main());
    t1.start();
    t1.join();
    while 1>0:
        try:
            time.sleep(25);
            f = open('result.txt','r');
            result = f.read();
            result_obj = eval(result);
            image = get(result_obj['url']).content;
            time.sleep(5);
            if image:
                context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="")])
                context.bot.send_message(chat_id=update.effective_chat.id, text=result_obj['message']);
                context.bot.send_message(chat_id=update.effective_chat.id, text=result_obj['name']); 
                f = open('result.txt','w');
                result = f.write('');
                f.close();

        except Exception:
            traceback.print_exc();

def messageHandler(update: Update, context: CallbackContext):
    print('Kaka');
    
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling();

