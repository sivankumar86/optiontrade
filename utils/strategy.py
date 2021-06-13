# These are standard strategies to be used at your own risk only after complete information.

class strategies:

    def __init__(self,broker):
        self.Client = broker

    def get_scripcode(self, symbol, strike, expiry, opt):
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
        year = expiry[:4]
        symbol = symbol.upper()
        strike_f = "{:.2f}".format(float(strike))
        sym = f'{symbol} {date} {mon} {year} {opt} {strike_f}'
        req = [
            {"Exch": "N", "ExchType": "D", "Symbol": sym, "Expiry": expiry, "StrikePrice": strike, "OptionType": opt}]
        res = self.Client.fetch_market_feed(req)
        token = res['Data'][0]['Token']
        return token

    def intraday(self, intra):
        if intra == 'I':
            return True
        else:
            return False

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

        order_status = self.Client.place_order(scrip)
        print(order_status)


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
