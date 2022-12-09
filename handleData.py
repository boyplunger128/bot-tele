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


def main():
    f1 = open('listCoins.txt','r');
    f2 = open('result.txt','w');
    listCoins = Convert(f1.read());
    while 1>0:
        for coin in listCoins:
            try:
                result ={
                    "url":"",
                    "name":"",
                    "message":""
                }
                #print(coin);
                coinHis = handleAPI.getHistoryCandle(coin);
                #print(coinHis);
                time.sleep(2);
                openPrice = coinHis[0][1];
                closePrice = coinHis[0][4];
                messageBox ='';
                flag20 = 0;
                flag100 = 0;
                maValues = handleAPI.getMultiIndiValue(coin,'1h');
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
                    f2.write(str(result));
                    print(result);
                    f2.close();
                    time.sleep(5);
                    
            except Exception:
                traceback.print_exc();  
                time.sleep(1); 
    time.sleep(3);      
        

