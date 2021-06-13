from flask import Flask, render_template

from tradeapi.samcoAPI import SamcoCalls
from flask import request

from ddb import dynamodbops as ddb
import uuid

app = Flask(__name__)
samco=SamcoCalls("")


@app.route("/")
def home():
  return optionview()

@app.route("/about")
def about():
  return render_template("about.html")

def buildoptions(symbol):
  strike = symbol[-7:-2]
  strike2 = int(strike) - 300;
  symbols=[]
  for i in range(6):
    strike2=strike2+100
    symbols.append(symbol.replace(strike, str(strike2)))
  return symbols

@app.route("/getquote")
def getquote():
  symbol = request.args.get('symbol')
  activity = request.args.get('activity')
  res=samco.getQuotes(symbol)
  bestprice= float(res["bestAsks"][0]["price"])-0.2 if (activity=="sell") else float(res["bestBids"][0]["price"])+0.2
  return {"strike":symbol[-7:-2],"ltp":res["lastTradedPrice"],"bestprice":bestprice}


@app.route("/spread")
def spread():
  symbol = request.args.get('symbol')
  strike=symbol[-7:-2]
  type=symbol[-2:]
  if (type=='PE'):
    strike2 = int(strike) - 300;
    name="Put Spread"
  else:
    strike2 = int(strike) +300;
    name="Call Spread"

  randomid = uuid.uuid1()
  id="{}_{}".format(name,randomid)
  leg1 = symbol
  leg2 = symbol.replace(strike, str(strike2))
  legs=[]
  legs.append({"symbol":leg1,"symbols":buildoptions(symbol),"strike":strike,"type":type,"activity":"SELL"})
  legs.append({"symbol":leg2,"symbols":buildoptions(symbol),"strike":strike2,"type":type,"activity":"BUY"})
  return render_template('spread.html', trade=legs,spreadname=name,id=id)

def limitoption(x):
  spot= 36000.00 if(x['spotPrice'].strip()=='') else float(x['spotPrice'])
  upperlimit=spot+5000
  lowerlimit=spot-5000
  return  float(x['strikePrice']) >lowerlimit and float(x['strikePrice']) <upperlimit

@app.route("/optionview")
def optionview():
  reponse=samco.optioncontract(
                         search_symbol_name='BANKNIFTY', expiry_date='2021-06-24')
  reduceoption=filter(limitoption,reponse['optionChainDetails'])
  return render_template('optionview.html', r=reduceoption)


@app.route("/placeOrder",methods = ['POST'])
def placeOrder():
    orders = request.form['orders']
    id = request.form['id']

   # res=samco.placeOrder(symbol,25,activity.strip(),bprice)
   # ddb.addentry({"id": id, "name": name, "symbol": symbol,
   #               "ordernumber":res['orderNumber'],"orderDetails":res["orderDetails"]})
   # print(res)
    #return {"ordernumber":res["orderNumber"],"id":id,"status":res["exchangeOrderStatus"]}
    return "test"

@app.route("/getorderstaus")
def getorderstaus():
    ordernumber = request.args.get('ordernumber')
    res=samco.getOrderStatus(ordernumber)
    print(res)
    return {"orderStatus":res["orderStatus"]}

@app.route("/position")
def positionview():
   res= samco.get_positions_data()
   print(res)
   reduceoption=res["positionDetails"]
   return render_template('position.html', r=reduceoption)




if __name__ == "__main__":
  app.run(debug=True)

  ##50477696