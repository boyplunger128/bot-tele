# import requests
#this is data for indicators values.
# API_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM4YzY4Y2JmYzVhOGFkZmVjODM5MmRmIiwiaWF0IjoxNjcwMTQ2MjUxLCJleHAiOjMzMTc0NjEwMjUxfQ.PgTZ3wuUns6LS7f7vGi7fOrNKcH62ZE-oHCtRbJ3jvM';
# INDICATOR='ma'
# EXCHANGE='binance'
# INTERVAL='1D'
# PERIOD20='20'
# PERIOD100='100'

# import time
# import requests;
# from telegram.ext import *
# from telegram import *

# #convert data to list
# def Convert(data):
#     datanew = data.strip("[]").split(', ')
#     return datanew;
# #get current price

# binance = requests.get('https://api.binance.com/api/v1/ticker/24hr')

# listBUSD = [];
# f = open('listCoins.txt','r');

# data = f.read();
# dataNew = Convert(data);

# f.close();
#create bot tele


# YOUR_API_KEY='zRIPWBrtSn84Y2OxnBEsVa8V0saLQvr864oZl4bX';
# SYMBOL='ETHUSDT';
# YOUR_CHAT_ID='5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w';
# TEST_CHAT_ID='5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w';

# def start_command(update,context):    
#     update.message.reply_text('Hello World!');
        
# def handle_message(update,context):
#     text=str(update.message.text).lower();
#     update.message.reply_text(text);
    
#     if(text=='getchart'):
#         try:
#             response = requests.get('https://api.chart-img.com/v1/tradingview/mini-chart/send/telegram?chatId={YOUR_CHAT_ID}&symbol=BINANCE:ETHUSDT&interval=3M&key={YOUR_API_KEY}');
#             update.message.reply_text('loading...');
#             time.sleep(10);
#             update.message.reply_text(str(response.json()));
#             image = requests.get('https://api.chart-img.com/v1/tradingview/advanced-chart?interval=4h&height=300&key={YOUR_API_KEY}')
#             context.bot.sendMediaGroup(chat_id=YOUR_CHAT_ID,media=[InputMediaPhoto(image,caption="")]);
#         except error:
#             update.message.reply_text(str(error));
    
# def error(update,context):
#     print('Error')


# def main():

#     # print('Starting bot...');
#     # updater = Updater(YOUR_CHAT_ID,use_context=True);
#     # dp = updater.dispatcher;
#     # dp.add_handler(CommandHandler("start",start_command))
#     # dp.add_handler(MessageHandler(Filters.text,handle_message))

#     # dp.add_error_handler(error);

#     # updater.start_polling()
#     # updater.idle()
#     # print('Bot started');

# main();  


# import time
# from requests import *;
# from telegram.ext import *
# from telegram import *

# YOUR_API_KEY='zRIPWBrtSn84Y2OxnBEsVa8V0saLQvr864oZl4bX';
# SYMBOL='ETHUSDT';
# YOUR_CHAT_ID='5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w';


# def main():
#     updater = Updater(token=YOUR_CHAT_ID);
#     dispatcher = updater.dispatcher;
#     print('starting bot...')
#     def startCommand(update: Update,context: CallbackContext):
#         update.message.reply_text('Hello mother fucker');
    
#     def  messageHandler(update: Update,context: CallbackContext):
#         text = str(update.message.text);       
     
#         if(text=='image'):
#             try:                
#                 update.message.reply_text('fetching image....');        
#                 image =get('https://api.chart-img.com/v1/tradingview/advanced-chart?interval=4h&height=300&key=zRIPWBrtSn84Y2OxnBEsVa8V0saLQvr864oZl4bX').content;       
#                 print(type(image));
#                 update.message.reply_text('fetch successfully');
#                 update.message.reply_text('please waiting for loading img....');
#                 time.sleep(5);
#                 if image:
#                     update.message.reply_text('We have image, but context...');                    
#                     context.bot.sendMediaGroup(YOUR_CHAT_ID,media=[InputMediaPhoto(image,caption="")]);
#             except:
#                 update.message.reply_text('Load failed');
                
#                 print('Bug is occured');
#         else:
#                 update.message.reply_text('type updating...');    

#     dispatcher.add_handler(CommandHandler("start",startCommand));
#     dispatcher.add_handler(MessageHandler(Filters.text,messageHandler));
#     updater.start_polling();
#     updater.idle();
# main()

# from telegram import *
# from telegram.ext import * 
# from requests import *

# updater = Updater(token="5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w")
# dispatcher = updater.dispatcher

# randomPeopleText = "Random Person"
# randomImageText = "Random Image"

# randomPeopleUrl = "https://api.chart-img.com/v1/tradingview/advanced-chart?interval=4h&height=300&key=zRIPWBrtSn84Y2OxnBEsVa8V0saLQvr864oZl4bX"
# randomPImageUrl = "https://picsum.photos/1200"

# likes = 0
# dislikes = 0

# allowedUsernames = ['tranbao981','Tran Bao']

# def startCommand(update: Update, context: CallbackContext):
#     buttons = [[KeyboardButton(randomImageText)], [KeyboardButton(randomPeopleText)]]
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))

# def messageHandler(update: Update, context: CallbackContext):
#     # if update.effective_chat.username not in allowedUsernames:
#     #     context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
#     #     return
#     if randomPeopleText in update.message.text:
#         image = get(randomPeopleUrl).content
#     if randomImageText in update.message.text:
#         image = get(randomPImageUrl).content

#     if image:
#         context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="")])

#         buttons = [[InlineKeyboardButton("👍", callback_data="like")], [InlineKeyboardButton("👎", callback_data="dislike")]]
#         context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Did you like the image?")

# def queryHandler(update: Update, context: CallbackContext):
#     query = update.callback_query.data
#     update.callback_query.answer()

#     global likes, dislikes

#     if "like" in query:
#         likes +=1
    
#     if "dislike" in query:
#         dislikes +=1

#     print(f"likes => {likes} and dislikes => {dislikes}")


# dispatcher.add_handler(CommandHandler("start", startCommand))
# dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
# dispatcher.add_handler(CallbackQueryHandler(queryHandler))

# updater.start_polling()

# f = open('result.txt','r');
# result = f.read();
# result_obj = eval(result);
# print(result_obj['url']);

# import os;
# from dotenv import load_dotenv,find_dotenv

# load_dotenv(find_dotenv());

# print(os.getenv('INTERVAL'));

import datetime;
import requests;
import time;
import os;
from dotenv import load_dotenv,find_dotenv;


load_dotenv(find_dotenv());

def getListCoins():
    request =  requests.get('https://api.binance.com/api/v1/ticker/24hr');
    time.sleep(5);
    datas = request.json();
    #print('Alls data is: ',datas);
    busdData = [];
    for data in datas:
         if('BUSD' in str(data['symbol'][slice(4)]) or 'BUSD' in str(data['symbol'][slice(len(data['symbol'])-4,len(data['symbol']))])):
            busdData.append(data);

    for i in range(len(busdData)):
        for j in range(len(busdData)):
            if(busdData[i]['priceChangePercent']>busdData[j]['priceChangePercent']):
                temp=busdData[i]
                busdData[i]=busdData[j];
                busdData[j]=temp; 
    listName = [];
    for i in range(int(os.getenv('AMOUNT_TOP_COIN'))):
        if('BUSD' in busdData[i]['symbol']):
            listName.append(busdData[i]['symbol']);
    #print(f.read());
    f = open('listCoins.txt','w');
    f.write(str(listName));
    f.close();
    return listName;

getListCoins();