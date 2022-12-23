# import time;
# import handleAPI;
# from telegram.ext import *
# from telegram import *
# import constants;
# from datetime import date;
# import threading;
# import os;
# from requests import *;
# import traceback;


# #convert data to list
# def Convert(data):
#     datanew = data.strip("[]").split(', ')
#     return datanew;

# d2 = 7;
# def t_updatelistCoins():
#     while 1>0:
#         d1 =date.today();
#         thisDay = d1.strftime("%d");
#         if(int(thisDay)!=d2):
#             handleAPI.getListCoins();
#             time.sleep(14400);


# def main():
#     f1 = open('listCoins.txt','r');
#     f2 = open('result.txt','w');
#     listCoins = Convert(f1.read());
#     while 1>0:
#         for coin in listCoins:
#             try:
#                 result ={
#                     "url":"",
#                     "name":"",
#                     "message":""
#                 }
#                 #print(coin);
#                 coinHis = handleAPI.getHistoryCandle(coin);
#                 #print(coinHis);
#                 time.sleep(2);
#                 openPrice = coinHis[0][1];
#                 closePrice = coinHis[0][4];
#                 messageBox ='';
#                 flag20 = 0;
#                 flag100 = 0;
#                 maValues = handleAPI.getMultiIndiValue(coin,'1h');
#                 time.sleep(2);
#                 if(float(openPrice) < maValues[0] and maValues[0] < float(closePrice)):
#                     flag20=1;
#                 if(float(openPrice) < maValues[1] and maValues[1] < float(closePrice)):
#                     flag20=1;
#                 if(flag100!=0):
#                     if(flag20!=0):
#                         messageBox = coin +' has passed MA100 & MA20';
#                     else:
#                         messageBox = coin +' has passed MA100';
#                 else:
#                         if(flag20!=0):
#                             messageBox = coin+' has passed Ma20';
#                         alertCoin = coin+' checked!';
#                 if(flag20!=0 or flag100!=0):
#                     Url = 'https://api.chart-img.com/v1/tradingview/advanced-chart?height=500&studies=MA:20&studies=MA:100&studies=RSI&symbol='+coin.strip("''")+'&key='+constants.YOUR_API_KEY_CHART;
#                     #print(Url);
#                     result['url']=Url;
#                     result['message']=messageBox;
#                     result['name']=coin.strip("''");
#                     f2.write(str(result));
#                     print(result);
#                     f2.close();
#                     time.sleep(5);
                    
#             except Exception:
#                 traceback.print_exc();  
#                 time.sleep(1); 
#     time.sleep(3);      
import datetime;
import requests;
import time;
import os;
from dotenv import load_dotenv,find_dotenv;


load_dotenv(find_dotenv());

def getHistoryCandle(SYMBOL,interval):    
    params = SYMBOL.strip("''");
    url = 'https://api.binance.com/api/v3/klines?symbol='+params+'&interval='+interval+'&limit=1';
    request =   requests.get(url);
    time.sleep(1);
    listData = request.json();
    print('requesting...');
    print(request);
    return listData;

SYMBOL='BTCUSDT'

def getMultiIndiValue(SYMBOL,interval):
    # preSymbol = SYMBOL.replace('USDT','');
    # LastSymol = preSymbol+'/USDT';
    # print('input value for indicheck',LastSymol);
    lastSymbol = SYMBOL.strip("''");
    print('symbol in indicator: ',lastSymbol);
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
                "period":os.getenv('PERIOD20'),
                "backtracks":3
            },
            {        
                "indicator": "ma",
                "period": os.getenv('PERIOD100'),
                "backtracks":3
            }
            ],
            
        }
    }
    
    response = requests.post(url = endpoint, json = parameters)
    time.sleep(2);
    # Extract data in json format 
    #print(response);
    data = response.json();
    result={
        "ma20_now":0,
        "ma20_past":0,
        "ma100_now":0,
        "ma100_past":0,
    }
    result["ma20_1"]=data['data'][1]['result'];
    result["ma20_2"]=data['data'][2]['result'];
    result["ma100_1"]=data['data'][4]['result'];
    result["ma100_2"]=data['data'][5]['result'];

    #print('result is: ',result);
    return result;

print(getMultiIndiValue(SYMBOL,'1h'));