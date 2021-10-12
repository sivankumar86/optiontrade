from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlite.tradebook import TradeBook

engine = create_engine('sqlite:////Users/srramas/tradedb/trade.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()


c1 = TradeBook(name = 'bn', symbol = 'bn', strike=30.0,oprice=1,cprice=0.0,expire='2020-10-10',strategy='putcredit',isactive=1)

session.add(c1)
session.commit()


result = session.query(TradeBook).all()

for row in result:
   print (row.name)