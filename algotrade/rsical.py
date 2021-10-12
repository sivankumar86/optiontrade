import configparser

import pandas as pd
from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json
from business_calendar import Calendar
import datetime

# normal calendar, no holidays
from algotrade.candleStickAnalyze import hammerPattern, shootingStar, piercing
from utils import email
from utils.dateutils import getday

cal = Calendar()
lastBusDay = datetime.datetime.today()
#lastBusDay = lastBusDay-datetime.timedelta(days = 1)

today=getday(lastBusDay,-1)
yesterday=getday(lastBusDay,-2)
tendaybk=getday(lastBusDay,-60)

def rsidivergenece(Data,company):
    lower_barrier = 30.0
    upper_barrier = 70.0
    width = 5
    details=[]
    rsi_index=Data.columns.get_loc("RSI")
    close_index=Data.columns.get_loc("ltp")
    # Bullish Divergence
    for i in range(len(Data)):
        details.append({"index":i,"status":"none"})
        try:
            # print(Data.iloc[i]["RSI"])
            if Data.iloc[i,rsi_index] < lower_barrier:
                for a in range(i + 1, i + width):
                    if Data.iloc[a, rsi_index] > lower_barrier:
                        for r in range(a + 1, a + width):
                            if Data.iloc[r, rsi_index] < lower_barrier and Data.iloc[r, rsi_index] > Data.iloc[i, rsi_index] and Data.iloc[
                                r, close_index] < Data.iloc[i, close_index]:
                                for s in range(r + 1, r + width):
                                    if Data.iloc[s, rsi_index] > lower_barrier:
                                        details[i]["status"]="bullish"
                                        #print('Bullish above', Data.iloc[s + 1, 1],company)
                                        Data.iloc[s + 1, 5] = 1
                                        break
                                    else:
                                        continue
                                else:
                                    continue
                        else:
                            continue
                else:
                    continue
        except IndexError:
            pass

    # Bearish Divergence
    for i in range(len(Data)):
        try:
            if Data.iloc[i, rsi_index] > upper_barrier:
                for a in range(i + 1, i + width):
                    if Data.iloc[a, rsi_index] < upper_barrier:
                        for r in range(a + 1, a + width):
                            if Data.iloc[r, rsi_index] > upper_barrier and Data.iloc[r, rsi_index] < Data.iloc[i, rsi_index] and Data.iloc[
                                r, close_index] > Data.iloc[i, close_index]:
                                for s in range(r + 1, r + width):
                                    if Data.iloc[s, rsi_index] < upper_barrier:
                                        details[i]["status"] = "bearish"
                                        #print('Bearish below', Data.iloc[s + 1, 2],company)
                                        Data.iloc[s + 1, 6] = -1
                                        break
                                    else:
                                        continue
                            else:
                                continue
                        else:
                            continue
                else:
                    continue
        except IndexError:
            pass
    return details

def rsiCalcualte(prices,numberofdays):
    i = 0
    upPrices=[]
    downPrices=[]
    #  Loop to hold up and down price movements
    while i < len(prices):
        if i == 0:
            upPrices.append(0)
            downPrices.append(0)
        else:
            if (prices[i]-prices[i-1])>0:
                upPrices.append(prices[i]-prices[i-1])
                downPrices.append(0)
            else:
                downPrices.append(prices[i]-prices[i-1])
                upPrices.append(0)
        i += 1
    x = 0
    avg_gain = []
    avg_loss = []
    #  Loop to calculate the average gain and loss
    while x < len(upPrices):
        if x <=numberofdays:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sumGain = 0
            sumLoss = 0
            y = x-numberofdays
            while y<=x:
                sumGain += upPrices[y]
                sumLoss += downPrices[y]
                y += 1
            avg_gain.append(sumGain/numberofdays)
            avg_loss.append(abs(sumLoss/numberofdays))
        x += 1
    p = 0
    RS = []
    RSI = []
    #  Loop to calculate RSI and RS
    while p < len(prices):
        if p <=numberofdays:
            RS.append(0)
            RSI.append(0)
        else:
            RSvalue = (avg_gain[p]/avg_loss[p])
            RS.append(RSvalue)
            RSI.append(100 - (100/(1+RSvalue)))
        p+=1
    #  Creates the csv for each stock's RSI and price movements
    df_dict = {
        'RSI' : RSI
    }
    df = pd.DataFrame(df_dict, columns = ["RSI"])
    return df




def technicalAnalysis(dfp,company):
    dfp['ltp'] = dfp['ltp'].astype(float)
    dfp['low'] = dfp['low'].astype(float)
    dfp['high'] = dfp['high'].astype(float)
    dfp['open'] = dfp['open'].astype(float)
    dfp['volume'] = dfp['volume'].astype(int)
    dfp['diff'] = dfp['open'] - dfp['ltp']
    dfp['Volume_SMA_20'] = dfp.iloc[:, 6].rolling(window=20).mean()
    dfp['Volume_SMA_10'] = dfp.iloc[:, 6].rolling(window=10).mean()
    dfp['Volume_SMA_10'] = dfp['Volume_SMA_10'].fillna(0)
    dfp['Volume_SMA_10'] = dfp['Volume_SMA_10'].round(0).astype(int)
    dfp['Volume_SMA_20'] = dfp['Volume_SMA_20'].fillna(0)
    dfp['Volume_SMA_20'] = dfp['Volume_SMA_20'].round(0).astype(int)
    crossoverAnalysis(dfp)
    ticker = pd.merge(dfp, rsiCalcualte(dfp["ltp"], 20), left_index=True, right_index=True)
    ticker['TP'] = (ticker['ltp'] + ticker['low'] + ticker['high']) / 3
    ticker['std'] = ticker['TP'].rolling(20).std(ddof=0)
    ticker['pchance'] =((dfp['ltp'].shift(10)-dfp['ltp'])/dfp['ltp'].shift(10))
    ticker['pchance']=ticker['pchance'].fillna(0)
    ticker['MATP'] = ticker['TP'].rolling(20).mean()
    ticker['BOLU'] = ticker['MATP'] + 2 * ticker['std']
    ticker['BOLD'] = ticker['MATP'] - 2 * ticker['std']
    rsir_df = pd.DataFrame(rsidivergenece(ticker,company))
    ticker = pd.merge(ticker, rsir_df, left_index=True, right_index=True)
    ticker=hammerPattern(ticker)
    ticker=shootingStar(ticker)
    ticker=piercing(ticker)
    twodaybf=getday(lastBusDay,-4)
    twodaybfdf = ticker[ticker.date == twodaybf]
    todaydf = ticker[ticker.date == today]
    todayrsi = todaydf.RSI.item()
    yesdf = ticker[ticker.date == yesterday]
    tdbcsma =twodaybfdf.price_SMA_20.item()-twodaybfdf.price_SMA_5.item()
    todaycsma = todaydf.price_SMA_20.item() - todaydf.price_SMA_5.item()
    yesrsi=yesdf.RSI.item()
    bu = todaydf.BOLU.item()
    bl = todaydf.BOLD.item()
    ltp = todaydf.ltp.item()
    pma = todaydf.MATP.item()
    vma = todaydf.Volume_SMA_10.item()
    vol = todaydf.volume.item()
    volpercentage = 0
    if(vol>0):
     volpercentage = round(((vol - vma) / vma) * 100)
    status={"symbol": symbol, "rsi":round(todayrsi),"vpercent":volpercentage,"price":todaydf.ltp.item(),
            "day":today,"MA":round(todaydf.MATP.item()),
            "10dpdper":round(todaydf.pchance.item()*100),
            "vol":round(todaydf.volume.item()/100000)}
    status["rsidiff"] = round(yesrsi - todayrsi)
    status["pdiff"] = round(todaydf.ltp.item() - yesdf.ltp.item())
    status["SELL_PUT"]=""
    status["SELL_CALL"]=""
    if (abs(volpercentage)< 25 or volpercentage==0):
        if (todaydf.status.item()=='bullish'):
            status["SELL_PUT"] = status["SELL_PUT"]+", RSIDIV"
        if (todaydf.status.item()=='bearish'):
            status["SELL_CALL"] = status["SELL_CALL"]+", RSIDIV"
        if (todaydf.pchance.item() >9):
            status["SELL_PUT"] = status["SELL_PUT"]+", PC"
        if (todaydf.pchance.item() <-9):
            status["SELL_CALL"] = status["SELL_CALL"]+", PC"
        if(( todaydf['hammer'].item() or todaydf['piercing'].item()) and (volpercentage >-7)):
            if(todaydf['bpc'].item() >=3 ):
                status["SELL_PUT"] = status["SELL_PUT"] + ", CANDHP"
                if (todaycsma < 0 and tdbcsma > 0):
                    status["SELL_PUT"] = status["SELL_PUT"] + ", CMA"
                if (todayrsi < 45 and todayrsi - yesrsi > 2):
                    if (abs(bl - ltp) < abs(ltp - pma)):
                        status["SELL_PUT"] =status["SELL_PUT"] + "RSI"
        if(todaydf['shotingstar'].item() and  (todaydf['bpc'].item() <= 2 and (volpercentage >-7)
                                          )):
            status["SELL_CALL"] = status["SELL_CALL"] + ", CANDS"
            if ((todaycsma > 0 and tdbcsma < 0)):
                status["SELL_CALL"] = status["SELL_CALL"] + ", CMA"
            if (todayrsi > 80 and yesrsi - todayrsi >= 1):
                if (abs(bu - ltp) < abs(ltp - pma)):
                    status["SELL_CALL"] = status["SELL_CALL"] +"RSI"

    if(status["SELL_PUT"] !="" or status["SELL_CALL"]!=""):
        return status

    return None


def crossoverAnalysis(dfp):
    dfp['price_SMA_20'] = dfp['ltp'].rolling(window=20).mean()
    dfp['price_SMA_20'] = dfp['price_SMA_20'].fillna(0)
    dfp['price_SMA_20'] = dfp['price_SMA_20'].round(0).astype(int)
    dfp['price_SMA_5'] = dfp['ltp'].rolling(window=5).mean()
    dfp['price_SMA_5'] = dfp['price_SMA_5'].fillna(0)
    dfp['price_SMA_5'] = dfp['price_SMA_5'].round(0).astype(int)


file=open("/Users/srramas/Downloads/hightliquititystock.txt","r")
lines = file.readlines()
samco = StocknoteAPIPythonBridge()
config = configparser.ConfigParser()
config.read('../config/app.conf')
login = json.loads(samco.login(body={"userId": config.get("SAMCO","USERNAME"), 'password': config.get("SAMCO","PASSWORD"), 'yob': config.get("SAMCO","DOB")}))
print(login)
samco.set_session_token(sessionToken=login['sessionToken'])

statistics=[]

for symbol in lines:
    symbol=symbol.replace("\n","")
    res = json.loads(
        samco.get_historical_candle_data(symbol_name=symbol.strip(), exchange=samco.EXCHANGE_NSE, from_date=tendaybk,
                                         to_date=today))
    df = pd.json_normalize(res['historicalCandleData'])
    output=technicalAnalysis(df,symbol.strip())
    if(output):
        statistics.append(output)

for symbol in ["NIFTY 50","NIFTY BANK"]:
    res = json.loads(samco.get_index_candle_data(index_name=symbol.strip(), from_date=tendaybk,to_date=today))
    df = pd.json_normalize(res['indexCandleData'])
    #print(df)
    output = technicalAnalysis(df, symbol.strip())
    if (output):
        statistics.append(output)

df=pd.DataFrame(statistics)
#df['vol']=df['vol'].astype(int)
#out=df.sort_values(by=['vol'],ascending=False).reset_index(drop=True)
email.send_email(df.to_html(),"Indian Stock Oppurity - {}".format(today))
# print(out.to_html())

