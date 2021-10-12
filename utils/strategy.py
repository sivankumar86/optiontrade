# These are standard strategies to be used at your own risk only after complete information.
import math
import logging

class strategies:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    def __init__(self,broker):
        self.Client = broker

    def get_scripcode(self, symbol, strike, expiry, opt,etype):
        month = {
            "01": 'JAN',
            "02": 'FEB',
            "03": 'MAR',
            "04": 'APR',
            "05": 'MAY',
            "06": 'JUN',
            "07": 'JUL',
            "08": 'AUG',
            "09": 'SEP',
            "10": 'OCT',
            "11": 'NOV',
            "12": 'DEC'
        }
        date = expiry[6:]
        mon = month[expiry[4:6]]
        year = expiry[2:4]
        symbol = symbol.upper()
        if(etype=="m"):
            sym=f'{symbol}{year}{mon}{strike}{opt}'
        else:
            sym=f'{symbol}{date}{mon}{year}{strike}{opt}'

        res=self.Client.getQuotes(symbol=sym)

        return res



    def short_straddle(self, symbol, strike, qty, expiry, intra):
        self.symbol = symbol
        self.strike = strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        scrip = []
        options = ['CE', 'PE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.strike, self.expiry, opt)
            scrip.append(sc)

        order_status = self.Client.placeOrder(scrip)
        print(order_status)

    def credit_call(self, symbol,sellstrike,buystrike, qty, expiry, etype):
        self.symbol = symbol
        self.buystrike = buystrike
        self.sellstrike = sellstrike
        self.qty = qty
        self.expiry = expiry
        self.etype = etype
        scrip = []
        option = 'CE'
        if (sellstrike > buystrike):
            return "buystrike less than sellstrike"

        sc = self.get_scripcode(self.symbol, self.buystrike, self.expiry, option,etype)
        if (abs(float(sc["bestAsks"][0]["price"])-float(sc["bestBids"][0]["price"])) <=2.0):
            scrip.append({"symbol":sc['tradingSymbol'],"quantity":qty,"tradetype":self.Client.TRANSACTION_TYPE_BUY,"bprice":math.ceil(float(sc["bestAsks"][0]["price"]))-0.20})
        else:
            return "not eligible bc of first"
        sc = self.get_scripcode(self.symbol, self.sellstrike, self.expiry, option,etype)
        if (abs(float(sc["bestAsks"][0]["price"])-float(sc["bestBids"][0]["price"])) <=2.0):
         scrip.append({"symbol":sc['tradingSymbol'],"quantity":qty,"tradetype":self.Client.TRANSACTION_TYPE_SELL,"bprice":math.ceil(float(sc["bestBids"][0]["price"]))-0.50})
        else:
            return "not eligible bc of second"
        status=[]
        logging.info(scrip)
        for order in scrip:
            order_status = self.Client.placeOrder(**order)
            logging.info(order_status)
            status.append(order_status)
            if order_status['status'] == 'Success':
                 continue
            else:
                 logging.info('Order process failed !')
                 break

        return status


    def credit_put(self, symbol,sellstrike,buystrike, qty, expiry, etype):
        self.symbol = symbol
        self.buystrike = buystrike
        self.sellstrike = sellstrike
        self.qty = qty
        self.expiry = expiry
        self.etype = etype
        scrip = []
        option = 'PE'
        if(buystrike>sellstrike):
            return "buystrike greater than sellstrike"
        sc = self.get_scripcode(self.symbol, self.buystrike, self.expiry, option,etype)
        #print(sc)
        if (abs(float(sc["bestAsks"][0]["price"])-float(sc["bestBids"][0]["price"])) <2.0):
            scrip.append({"symbol":sc['tradingSymbol'],"quantity":qty,"tradetype":self.Client.TRANSACTION_TYPE_BUY,"bprice":math.ceil(float(sc["bestAsks"][0]["price"]))-0.20})
        else:
            return "not eligible bc of first"
        sc = self.get_scripcode(self.symbol, self.sellstrike, self.expiry, option,etype)
        if (abs(float(sc["bestAsks"][0]["price"])-float(sc["bestBids"][0]["price"])) <2.0):
         scrip.append({"symbol":sc['tradingSymbol'],"quantity":qty,"tradetype":self.Client.TRANSACTION_TYPE_SELL,"bprice":math.ceil(float(sc["bestBids"][0]["price"]))-0.50})
        else:
            return "not eligible bc of second"
        status=[]
        print(scrip)
        for order in scrip:
            order_status = self.Client.placeOrder(**order)
            print(order_status)
            status.append(order_status)
            if order_status['status'] == 'Success':
                 continue
            else:
                 break

        return status

    def short_strangle(self, symbol, strike, qty, expiry, intra):
        strike.sort()
        self.symbol = symbol
        self.strike = strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        scrip = []
        i = 0
        options = ['PE', 'CE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.strike[i], self.expiry, opt)
            i = i + 1
            scrip.append(sc)
        order_status = self.Client.place_order(scrip)

    def long_straddle(self, symbol, strike, qty, expiry, intra):
        self.symbol = symbol
        self.strike = strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        scrip = []
        options = ['CE', 'PE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.strike, self.expiry, opt)
            scrip.append(sc)

        order_status = self.Client.place_order(scrip)

    def long_strangle(self, symbol, strike, qty, expiry, intra):
        strike.sort()
        self.symbol = symbol
        self.strike = strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        scrip = []
        i = 0
        options = ['PE', 'CE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.strike[i], self.expiry, opt)
            i = i + 1
            scrip.append(sc)
        order_status = self.Client.place_order(scrip)

    def iron_fly(self, symbol, buy_strike, sell_strike, qty, expiry, intra):
        buy_strike.sort()
        self.symbol = symbol
        self.buy_strike = buy_strike
        self.sell_strike = sell_strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        buy_scrip = []
        sell_scrip = []
        i = 0
        options = ['PE', 'CE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.buy_strike[i], self.expiry, opt)
            i = i + 1
            buy_scrip.append(sc)
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.sell_strike, self.expiry, opt)
            sell_scrip.append(sc)
        order_status = self.Client.place_order(buy_scrip)
        order_status = self.Client.place_order(sell_scrip)

    def iron_condor(self, symbol, buy_strike, sell_strike, qty, expiry, intra):
        buy_strike.sort()
        sell_strike.sort()
        self.symbol = symbol
        self.buy_strike = buy_strike
        self.sell_strike = sell_strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        buy_scrip = []
        sell_scrip = []
        i = 0
        j = 0
        options = ['PE', 'CE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.buy_strike[i], self.expiry, opt)
            i = i + 1
            buy_scrip.append(sc)
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.sell_strike[j], self.expiry, opt)
            j = j + 1
            sell_scrip.append(sc)
        order_status = self.Client.place_order(buy_scrip)
        order_status = self.Client.place_order(sell_scrip)

    def call_calendar(self, symbol, strike, qty, expiry, intra):
        self.symbol = symbol
        self.strike = strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        scrip = []
        i = 0
        options = ['CE', 'CE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.strike, self.expiry[i], opt)
            scrip.append(sc)
            i = i + 1
        order_status = self.Client.place_order(scrip)

    def put_calendar(self, symbol, strike, qty, expiry, intra):
        self.symbol = symbol
        self.strike = strike
        self.qty = qty
        self.expiry = expiry
        self.intra = intra
        scrip = []
        i = 0
        options = ['PE', 'PE']
        for opt in options:
            sc = self.get_scripcode(self.symbol, self.strike, self.expiry[i], opt)
            scrip.append(sc)
            i = i + 1
        order_status = self.Client.place_order(scrip)
