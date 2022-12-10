import time;
from telegram.ext import *
from telegram import *
import constants;
from datetime import date;
import threading;
import os;
from requests import *;
import traceback;
import requests;
#handle API


def getListCoins():
    request =  requests.get('https://api.binance.com/api/v1/ticker/24hr');
    time.sleep(5);
    datas =request.json();
    #print(len(datas));
    busdData = [];
    for data in datas:
        if('BUSD' in data['symbol']):
            busdData.append(data);

    for i in range(len(busdData)):
        for j in range(len(busdData)):
            if(busdData[i]['priceChangePercent']>busdData[j]['priceChangePercent']):
                temp=busdData[i]
                busdData[i]=busdData[j];
                busdData[j]=temp; 
    listName = [];
    for i in range(100):
        if('BUSD' in busdData[i]['symbol']):
            listName.append(busdData[i]['symbol']);
    #print(f.read());
    return listName;

def getHistoryCandle(SYMBOL):    
    params = SYMBOL.strip("''");
    url = 'https://api.binance.com/api/v3/klines?symbol='+params+'&interval=1h&limit=2';
    request =   requests.get(url);
    time.sleep(5);
    listData = request.json();
    print('requesting...');
    print(request);
    return listData;

def getMaValue(SYMBOL,PERIOD):
    preSymbol = SYMBOL.replace('BUSD','');
    LastSymol = preSymbol+'/BUSD';
    print(LastSymol);
    SecretKey = constants.API_KEY_INDIC;

    url = 'https://api.taapi.io/ma?secret='+SecretKey+'&exchange=binance&symbol='+LastSymol+'&interval=1h&period='+PERIOD;
    request =   requests.get(url);
    time.sleep(3);
    data = request.json();
    return data['value'];

def getMultiIndiValue(SYMBOL,interval):
    # preSymbol = SYMBOL.replace('BUSD','');
    # LastSymol = preSymbol+'/BUSD';
    # print('input value for indicheck',LastSymol);
    lastSymbol = SYMBOL.strip("''");
    print('last symbol:',lastSymbol);
    endpoint = "https://api.taapi.io/bulk";
    
    # Define a JSON body with parameters to be sent to the API 
    parameters ={
        "secret": constants.API_KEY_INDIC,
        "construct": {
            "exchange": "binance",
            "symbol": lastSymbol,
            "interval": interval,
            "indicators": [             
            {
                "indicator":"ma",
                "period":20
            },
            {        
                "indicator": "ma",
                "period": 100 
            }
            ]
        }
    }
    
    # Send POST request and save the response as response object 
    response = requests.post(url = endpoint, json = parameters)
    time.sleep(3);
    # Extract data in json format 
    print(response);
    data = response.json();
    result = [];
    result.append(data['data'][0]['result']['value'])
    result.append(data['data'][1]['result']['value'])

    print('result is: ',result);
    return result;


#convert data to list

def Convert(data):
    datanew = data.strip("[]").split(', ')
    return datanew;


d2 = date.today();
def t_updatelistCoins():
    d1 =date.today();
    thisDay = d1.strftime("%d");
    if(int(thisDay)!=d2):
        getListCoins();

updater = Updater(token="5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w");
dispatcher = updater.dispatcher;

def startCommand(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to crypto hunter");
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait... Bot is checking... ^^");
    
    listCoins = getListCoins();

    print(listCoins);
    def execbot(result):
        try:
            #result_obj = eval(result); -- convert string to object, but is no need now
            image = get(result['url']).content;
            time.sleep(5);
            if image:
                context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="")])
                context.bot.send_message(chat_id=update.effective_chat.id, text=result['message']);
                context.bot.send_message(chat_id=update.effective_chat.id, text=result['name']); 
        except Exception:
            traceback.print_exc();
        time.sleep(5);
    i=0;
    def task():
        if(i%1440==0):
            t_updatelistCoins();

        for coin in listCoins:
            try:
                result ={
                    "url":"",
                    "name":"",
                    "message":""
                }
                #print(coin);
                coinHis = getHistoryCandle(coin.strip("''"));
                print(coinHis);
                time.sleep(2);
                openPrice = coinHis[0][1];
                closePrice = coinHis[0][4];
                messageBox ='';
                flag20 = 0;
                flag100 = 0;
                maValues = getMultiIndiValue(coin,'1h');
                time.sleep(2);
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
                    #print(Url);
                    result['url']=Url;
                    result['message']=messageBox;
                    result['name']=coin.strip("''");
                   
                    print(result);
        
                    time.sleep(5);
                    execbot(result);
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=alertCoin);
            except Exception:
                traceback.print_exc();  
                time.sleep(1); 
    i=i+1;


    context.job_queue.run_repeating(task(),1800,context=update.effective_chat.id);    
   
    

def messageHandler(update: Update, context: CallbackContext):
    print('Kaka');
    
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling();

