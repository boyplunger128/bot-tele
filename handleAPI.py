import requests;
import constants;
from telegram import *
from telegram.ext import * 
from requests import *
import time;

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

    f=open('listCoins.txt','w');
    listName = [];
    for i in range(100):
        if('BUSD' in busdData[i]['symbol']):
            listName.append(busdData[i]['symbol']);
    f.write(str(listName));
    f.close();

    f = open('listCoins.txt','r');
    #print(f.read());

    f.close();

def getHistoryCandle(SYMBOL):    
    params = SYMBOL.strip("''");
    url = 'https://api.binance.com/api/v3/klines?symbol='+params+'&interval=1h&limit=2';
    request =   requests.get(url);
    time.sleep(5);
    listData = request.json();
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



