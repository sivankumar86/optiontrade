# package import statement
from smartapi import SmartConnect  # or from smartapi.smartConnect import SmartConnect

# import smartapi.smartExceptions(for smartExceptions)

# create object of call
obj = SmartConnect(api_key="DW73g7kC")
                   # optional
                   # access_token = "your access token",
                   # refresh_token = "your refresh_token")

                   # login api call

data=obj.generateSession("P103324", "L@cky@07")
refreshToken = data['data']['refreshToken']

# fetch the feedtoken
feedToken = obj.getfeedToken()

# fetch User Profile
position = obj.position()
print(position)
# place order
try:
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": "BANKNIFTY26MAY2236600CE",
        "symboltoken": "52836",
        "transactiontype": "SELL",
        "exchange": "NFO",
        "ordertype": "LIMIT",
        "producttype": "CARRYFORWARD",
        "duration": "DAY",
        "price": "702",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": "25",
        "ordertag":"cs_may22"
    }
    #orderId = obj.placeOrder(orderparams)
    #print("The order id is: {}".format(orderId))

except Exception as e:
    print("Order placement failed: {}".format(e.message))
