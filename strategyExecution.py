import configparser
from time import time
import logging

from tradeapi.samcoAPI import SamcoCalls
from utils.strategy import strategies

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()

config.read('config/app.conf')

samco = SamcoCalls(
    {"userId": config.get("SAMCO","USERNAME"), 'password': config.get("SAMCO","PASSWORD"), 'yob': config.get("SAMCO","YOB")})


#out=samco.get_positions_data()

print(samco.getLimits())

position_output=samco.get_positions_data()

currentstatus={}

for ep in position_output['positionDetails']:
    currentstatus[ep['tradingSymbol']]=ep['unrealizedGainAndLoss']

print(currentstatus)

option_stra={
    "bankcallspread":["BANKNIFTY22AUG35500CE","BANKNIFTY22AUG36000CE"],
"niftycallspread":["NIFTY22AUG16500CE","NIFTY22AUG16400CE"]
}

for ps in option_stra.keys():
    profit=0
    for symbol in option_stra[ps]:
        profit=profit+float(currentstatus[symbol].replace(",",""))
    print(f"profit for {ps}: "+str(profit))


sg=strategies(samco)
##NIFTY
##BANKNIFTY
#print(samco.optioncontract("BANKNIFTY","2021-07-01"))
ts = time()
#print(sg.credit_put("banknifty",35500,35000,25,'20220813','m'))
#print(sg.credit_call("NIFTY",16400,16500,100,'20220813','m'))

#print(sg.debit_call("banknifty",36500,36700,25,'20220428','m'))

#print(sg.debit_put("banknifty",35800,36100,50,'20220106','w'))
#print(sg.debit_call("banknifty",36200,36000,50,'20220106','w'))

logging.info('Took %s seconds', time() - ts)