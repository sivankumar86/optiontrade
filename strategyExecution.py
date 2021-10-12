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
    {"userId": config.get("SAMCO","USERNAME"), 'password': config.get("SAMCO","PASSWORD"), 'yob': config.get("SAMCO","DOB")})


#out=samco.get_positions_data()

print(samco.getLimits())

sg=strategies(samco)

#print(samco.optioncontract("BANKNIFTY","2021-07-01"))
ts = time()
#print(sg.credit_put("banknifty",36500,35500,50,'20211014','w'))
print(sg.credit_call("banknifty",39000,39500,50,'20211014','w'))
logging.info('Took %s seconds', time() - ts)