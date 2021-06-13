from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json

class SamcoCalls():

    def __init__(self,sessionToken):
        self.samco = StocknoteAPIPythonBridge()
        self.samco.set_session_token(sessionToken=sessionToken)
    def optioncontract(self,search_symbol_name,expiry_date):
        return json.loads(self.samco.get_option_chain(search_symbol_name=search_symbol_name, exchange=self.samco.EXCHANGE_NFO,
                                     expiry_date=expiry_date))

    def getQuotes(self,symbol):
        return json.loads(self.samco.get_quote(symbol_name=symbol, exchange=self.samco.EXCHANGE_NFO))

    def placeOrder(self,symbol,quantity,type,bprice):
        return json.loads(self.samco.place_order(body={
            "symbolName": symbol,
            "exchange": self.samco.EXCHANGE_NFO,
            "transactionType": type,
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




