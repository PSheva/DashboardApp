from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Account(BaseModel):
    account_number: int
    balance: float
    equity: float
    export_time: datetime
    day_profit: Optional[float] = 0.0  
    week_profit: Optional[float] = 0.0  
    month_profit: Optional[float] = 0.0 
    day_equity: Optional[float] = 0.0
    strategy_name: Optional[str] = 'Default'
    p_l: Optional[float] = 0.0

    class Config:
        from_attributes = True

class OpenPosition(BaseModel):
    account_number: int
    ticket: int
    magic: int
    open_time: Optional[datetime]
    size: float
    symbol: str
    type: str
    open_price: Optional[float]
    tp_sl: Optional[float]
    profit: float

    class Config:
        from_attributes = True

class ClosedPosition(BaseModel):
    account_number: int
    ticket: int
    magic: int
    open_time: Optional[datetime]
    close_time: Optional[datetime]
    size: float
    symbol: str
    type: str
    open_price: float
    close_price: float
    tp_sl: Optional[float]
    profit: float

    class Config:
        from_attributes = True

class BalanceOperation(BaseModel):
    account_number: int
    ticket: int
    export_time: datetime
    profit: float
    comment: Optional[str] = None
    type: str

    class Config:
        from_attributes = True


class DashboardData(BaseModel):
    accounts: List[Account]
    total_balance: float
    total_equity: float
    total_day_profit: float
    total_day_equity: float
    total_week_profit: float 
    total_month_profit: float  
    open_positions: List[OpenPosition]
    closed_positions: List[ClosedPosition]
    balance_operations: List[BalanceOperation]
    last_export_time: Optional[datetime]

    class Config:
        from_attributes = True

class AccountInfoBase(BaseModel):
    account_number: int
    strategy_name: str
    broker_name: str

class AccountInfoCreate(AccountInfoBase):
    pass

class AccountInfo(AccountInfoBase):
    id: int

    class Config:
        from_attributes = True
