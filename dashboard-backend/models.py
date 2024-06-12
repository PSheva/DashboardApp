# models.py
from sqlalchemy import Column, Integer, Float, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AccountData(Base):
    __tablename__ = 'account_data'
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, index=True)
    export_time = Column(TIMESTAMP, index=True)
    balance = Column(Float)
    equity = Column(Float)
    p_l = Column(Float)
    margin = Column(Float)
    free_margin = Column(Float)

class TradeData(Base):
    __tablename__ = 'trade_data'
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer, index=True)
    ticket = Column(Integer)
    magic = Column(Integer)
    type = Column(String(30))
    symbol = Column(String(20))
    lots = Column(Float)
    open_time = Column(TIMESTAMP)
    close_time = Column(TIMESTAMP, nullable=True)
    open_price = Column(Float)
    close_price = Column(Float)
    current_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    profit = Column(Float)
    swap = Column(Float)
    commission = Column(Float)
    expiration = Column(TIMESTAMP, nullable=True)
    comment = Column(String(100))
    export_time = Column(TIMESTAMP)
