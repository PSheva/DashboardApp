# models.py
from sqlmodel import Field, SQLModel
from db import Base
from sqlalchemy import Column, Integer, Float, Text, TIMESTAMP, PrimaryKeyConstraint

class CurrentDataFrame(Base):
    __tablename__ = 'current_dataframe'

    account_number = Column("Account Number", Integer, primary_key=True, nullable=False)
    ticket = Column("Ticket", Float, nullable=True)
    magic = Column("Magic", Integer, nullable=False)
    ops_type = Column("Type", Integer, nullable=False)
    symbol = Column("Symbol", Integer, nullable=False)
    lots = Column("Lots", Float, nullable=False)
    open_time = Column("Open Time", TIMESTAMP(timezone=False), nullable=False)
    close_time = Column("Close Time", TIMESTAMP(timezone=False), nullable=False)
    open_price = Column("Open Price", Float, nullable=False)
    close_price = Column("Close Price", Float, nullable=False)
    current_price = Column("Current Price", Float, nullable=False)
    stop_loss = Column("Stop Loss", Float, nullable=False)
    take_profit = Column("Take Profit", Float, nullable=False)
    profit = Column("Profit", Float, nullable=False)
    swap = Column("Swap", Float, nullable=False)
    commsion = Column("Commission", Float, nullable=False)
    expiration = Column("Expiration", TIMESTAMP(timezone=False), nullable=False)
    comment = Column("Comment", Text, nullable=False)
    export_time = Column("Export Time", TIMESTAMP(timezone=False), nullable=False)
    balance = Column("Balance", Float, nullable=False)
    equity = Column("Equity", Float, nullable=False)
    p_l = Column("P/L", Float, nullable=False)
    margin = Column("Margin", Float, nullable=False)
    free_margin = Column("Free Margin", Float, nullable=False)



class Book(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    title:str
    author:str
    year:str

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

    
