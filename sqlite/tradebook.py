from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()
engine = create_engine('sqlite:////Users/srramas/tradedb/trade.db', echo = True)

class TradeBook(Base):
   __tablename__ = 'tradebook'
   id = Column(Integer, primary_key=True)
   name = Column(String)
   symbol = Column(String)
   strike = Column(Numeric)
   oprice = Column(Numeric)
   cprice = Column(Numeric)
   expire = Column(String)
   strategy = Column(String)
   isactive = Column(Integer)


from sqlalchemy import MetaData
meta = MetaData()
Base.metadata.create_all(engine)

# conn.execute('''CREATE TABLE tradebook
#          (ID INTEGER PRIMARY KEY NOT NULL,
#          NAME           TEXT    NOT NULL,
#          symbol            TEXT     NOT NULL,
#          strike        REAL,
#          oprice         REAL,
#          cprice         REAL,
#          expire        TEXT,
#          strategy TEXT,
#          isactive INT,
#          lastdate NUMERIC);''')