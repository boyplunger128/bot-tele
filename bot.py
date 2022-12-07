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
        
    f = open('listCoins.txt','r');
    listCoins = Convert(f.read());
    while 1>0:
        for coin in listCoins:
            try:
                print(coin);
                coinHis = handleAPI.getHistoryCandle(coin);
                print(coinHis);
                time.sleep(5);
                openPrice = coinHis[0][1];
                closePrice = coinHis[0][4];
                messageBox ='';
                flag20 = 0;
                flag100 = 0;
                maValues = handleAPI.getMultiIndiValue(coin,'1h');
                time.sleep(5);
                if(float(openPrice) < maValues[0] and maValues[0] < float(closePrice)):
                    flag20=1;
                if(float(openPrice) < maValues[1] and maValues[1] < float(closePrice)):
                    flag20=1;
                if(flag100!=0):
                    if(flag20!=0):
                        messageBox = coin +' has passed MA100 & MA20';
                    else:
                        messageBox = coin +' has passed MA100';
                else:
                        if(flag20!=0):
                            messageBox = coin+' has passed Ma20';
                        alertCoin = coin+' checked!';
                if(flag20!=0 or flag100!=0):
                    Url = 'https://api.chart-img.com/v1/tradingview/advanced-chart?height=500&studies=MA:20&studies=MA:100&studies=RSI&symbol='+coin.strip("''")+'&key='+constants.YOUR_API_KEY_CHART;
                    print(Url);
                    image = get(Url).content;
                    time.sleep(5);
                    if image:
                        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="")])
                        time.sleep(3); 
                        context.bot.send_message(chat_id=update.effective_chat.id, text=messageBox);
                context.bot.send_message(chat_id=update.effective_chat.id, text=alertCoin); 
                time.sleep(5);      
            except Exception:
                traceback.print_exc();  
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sư phụ ơi, có lỗi xảy ra :( ");


def messageHandler(update: Update, context: CallbackContext):
    print('Kaka');
    
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()