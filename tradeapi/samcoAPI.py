from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json

class SamcoCalls():
    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    def __init__(self,credential):
        self.samco = StocknoteAPIPythonBridge()
        login = json.loads(self.samco.login(body=credential))
        self.samco.set_session_token(sessionToken=login['sessionToken'])

    def optioncontract(self,search_symbol_name,expiry_date):
        return json.loads(self.samco.get_option_chain(search_symbol_name=search_symbol_name, exchange=self.samco.EXCHANGE_NFO,
                                     expiry_date=expiry_date))

    def optioncontract_strike(self, search_symbol_name, strike_price,expiry_date,option_type):
        return json.loads(
            self.samco.get_option_chain(search_symbol_name=search_symbol_name,strike_price=strike_price, exchange=self.samco.EXCHANGE_NFO,
                                        expiry_date=expiry_date,option_type=option_type))

    def getQuotes(self,symbol):
        return json.loads(self.samco.get_quote(symbol_name=symbol, exchange=self.samco.EXCHANGE_NFO))

    def placeOrder(self,symbol,quantity,tradetype,bprice):
        return json.loads(self.samco.place_order(body={
            "symbolName": symbol,
            "exchange": self.samco.EXCHANGE_NFO,
            "transactionType": tradetype,
            "orderType": self.samco.ORDER_TYPE_LIMIT,
            "price": bprice,
            "quantity": quantity,
            "disclosedQuantity": "",
            "orderValidity": self.samco.VALIDITY_DAY,
            "productType": self.samco.PRODUCT_NRML,
            "afterMarketOrderFlag": "NO"
        }))

    def get_positions_data(self):
        return  json.loads(self.samco.get_positions_data(position_type=self.samco.POSITION_TYPE_NET))

    def getOrderStatus(self,ordernumber):
        return  json.loads(self.samco.get_order_status(order_number=ordernumber))

    def getLimits(self):
        return json.loads(self.samco.get_limits())








