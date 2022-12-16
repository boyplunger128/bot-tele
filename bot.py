import time;
import datetime;
from telegram.ext import *
from telegram import *
from datetime import date;
from requests import *;
import traceback;
import requests;
import os;
from dotenv import load_dotenv,find_dotenv;
from apscheduler.schedulers.blocking import BlockingScheduler;

#handle API

load_dotenv(find_dotenv());



def getListCoins():
    request =  requests.get('https://api.binance.com/api/v1/ticker/24hr');
    time.sleep(5);
    datas =request.json();
    #print('Alls data is: ',datas);
    busdData = [];
    for data in datas:
        if('USDT' in str(data['symbol'][slice(len(data['symbol'])-4,len(data['symbol']))])):
            busdData.append(data);

    for i in range(len(busdData)):
        for j in range(len(busdData)):
            if(busdData[i]['priceChangePercent']>busdData[j]['priceChangePercent']):
                temp=busdData[i]
                busdData[i]=busdData[j];
                busdData[j]=temp; 
    listName = [];
    for i in range(int(os.getenv('AMOUNT_TOP_COIN'))):
        if('USDT' in busdData[i]['symbol']):
            listName.append(busdData[i]['symbol']);
    #print(f.read());
    return listName;

def getHistoryCandle(SYMBOL,interval):    
    params = SYMBOL.strip("''");
    url = 'https://api.binance.com/api/v3/klines?symbol='+params+'&interval='+interval+'&limit=2';
    request =   requests.get(url);
    time.sleep(5);
    listData = request.json();
    print('requesting...');
    print(request);
    return listData;

def getMaValue(SYMBOL,PERIOD):
    preSymbol = SYMBOL.replace('BUSD','');
    LastSymol = preSymbol+'/BUSD';
    #print(LastSymol);
    SecretKey = os.getenv('API_KEY_INDIC');

    url = 'https://api.taapi.io/ma?secret='+SecretKey+'&exchange=binance&symbol='+LastSymol+'&interval='+os.getenv('INTERVAL2')+'&period='+PERIOD;
    request =   requests.get(url);
    time.sleep(3);
    data = request.json();
    return data['value'];

def getMultiIndiValue(SYMBOL,interval):
    # preSymbol = SYMBOL.replace('BUSD','');
    # LastSymol = preSymbol+'/BUSD';
    # print('input value for indicheck',LastSymol);
    lastSymbol = SYMBOL.strip("''");
    #print('last symbol:',lastSymbol);
    endpoint = "https://api.taapi.io/bulk";
    
    # Define a JSON body with parameters to be sent to the API 
    parameters ={
        "secret": os.getenv('API_KEY_INDIC'),
        "construct": {
            "exchange": "binance",
            "symbol": lastSymbol,
            "interval": interval,
            "indicators": [             
            {
                "indicator":"ma",
                "period":os.getenv('PERIOD20')
            },
            {        
                "indicator": "ma",
                "period": os.getenv('PERIOD100')
            }
            ]
        }
    }
    
    # Send POST request and save the response as response object 
    response = requests.post(url = endpoint, json = parameters)
    time.sleep(3);
    # Extract data in json format 
    #print(response);
    data = response.json();
    result = [];
    result.append(data['data'][0]['result']['value'])
    result.append(data['data'][1]['result']['value'])

    #print('result is: ',result);
    return result;


#convert data to list

def Convert(data):
    datanew = data.strip("[]").split(', ')
    return datanew;


d2 = date.today();
def t_updatelistCoins():
    getListCoins();

updater = Updater(token="5960253722:AAEl6Qn62IOWT-J5SkL0LavLe8E_9ObRT3w");
dispatcher = updater.dispatcher;

def startCommand(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to crypto hunter");
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait... Bot is checking... ^^");
   
    listCoins = getListCoins();

    #print(listCoins);
    def execbot(result):
        try:
            #result_obj = eval(result); -- convert string to object, but is no need now
            image = get(result['url']).content;
            symbol = result['name'].replace('BUSD','');
            link_buy = result['message']+'\n\nYou can buy it here:\nhttps://www.binance.com/vi/trade/'+symbol+'_BUSD?theme=dark&type=spot \n';
            time.sleep(5);
            if image:
                context.bot.sendMediaGroup(chat_id=int(result['channelID']), media=[InputMediaPhoto(image, caption=link_buy)]);
                #context.bot.send_message(chat_id=update.effective_chat.id, text=result['message']);
                #context.bot.send_message(chat_id=update.effective_chat.id, text=link_buy,disable_web_page_preview=True); 
        except Exception:
            traceback.print_exc();
        time.sleep(5);

    def task():      
        i=0;
        interval=os.getenv('INTERVAL1');
        channelID = os.getenv('CHANNEL1');
        
        now = datetime.datetime.now();

        currentHour = now.hour;
        currentDays = now.day;

        while(True):                
            currentRun = datetime.datetime.now();
            runningHour=currentRun.hour;
            runningDays=currentRun.day;

            if(runningHour>currentHour):
                if(runningHour%4==0):
                    interval=os.getenv('INTERVAL3');
                    channelID = os.getenv('CHANNEL3');
                else:
                    interval=os.getenv('INTERVAL2');
                    channelID = os.getenv('CHANNEL2');
                currentHour=runningHour;
            else:
                if(runningHour==1 and currentHour == 23):
                    currentHour=0;
                interval=os.getenv('INTERVAL1');
                channelID = os.getenv('CHANNEL1');

            #update day by day for month, year.

            if(runningDays > currentDays):
                currentDays=runningDays;
                interval=os.getenv('INTERVAL4');
                channelID = os.getenv('CHANNEL4');
            else:
                runningMonth = now.month;
                if(runningMonth==1 or runningMonth ==3 or runningMonth ==5 or runningMonth==7 or runningMonth==8 or runningMonth==10 or runningMonth == 12):
                    if(runningDays == 1 and currentDays ==31):
                        currentDays=0;                            
                else:
                    if(runningMonth==2):
                        currentYear = now.year;
                        if(currentYear % 4 == 0 and currentYear % 100 !=0 or currentYear % 400 !=0 ):
                            if(runningDays == 1 and currentDays == 29):
                                currentDays = 0;
                            else:
                                if(runningDays == 1 and currentDays == 28):
                                    currentDays = 0;
                        else:
                            if(runningDays== 1 and currentDays == 31):
                                currentDays = 0;

                    
            #qua ngay moi thi update lai cai currentHourse = 0, vi qua ngay moi thi thoi gian moi        
            if(i%24==0):
                t_updatelistCoins();

            for coin in listCoins:
                print('current interval:'+interval);
                print(coin,len(listCoins));
                try:
                    result ={
                        "url":"",
                        "name":"",
                        "message":"",
                        "channelID":channelID
                    }
                    #print(coin);
                        
                    coinHis = getHistoryCandle(coin.strip("''"),interval);
                    #print(coinHis);
                    time.sleep(2);
                    openPrice = coinHis[0][1];
                    closePrice = coinHis[0][4];
                    messageBox ='';
                    flag20 = 0;
                    flag100 = 0;
                    maValues = getMultiIndiValue(coin,interval);
                    time.sleep(2);
                    if(float(openPrice) < maValues[0] and maValues[0] < float(closePrice)):
                        flag20=1;
                    if(float(openPrice) < maValues[1] and maValues[1] < float(closePrice)):
                        flag100=1;
                    if(flag100!=0):
                        if(flag20!=0):
                            messageBox ='\n'+ coin +' PASSED MA100 & MA20 AT '+interval.upper();
                        else:
                            messageBox ='\n'+coin +' PASSED MA100 AT '+interval.upper();
                    else:
                        if(flag20!=0):
                            messageBox ='\n'+ coin+' PASSED MA20 AT '+interval.upper();
                    if(flag20!=0):
                        #fix interval here
                        Url = 'https://api.chart-img.com/v1/tradingview/advanced-chart?interval='+interval+'&symbol='+coin+'&studies=MA:20&studies=RSI&key='+os.getenv('YOUR_API_KEY_CHART');
                        #print(Url);
                        result['url']=Url;
                        result['message']=messageBox;
                        result['name']=coin.strip("''");
                        
                        #print(result);
                
                        time.sleep(5);
                        execbot(result);
                    # else:
                        #context.bot.send_message(chat_id=update.effective_chat.id, text=alertCoin);
                except Exception:
                    traceback.print_exc();  
                    time.sleep(1); 
            i=i+1;
    task();
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is not supported for this channel or group!");
    print('bot stopped'); 


def messageHandler(update: Update, context: CallbackContext):
    print('Kaka');
    
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling(timeout=100);

