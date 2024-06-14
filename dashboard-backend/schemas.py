from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Account(BaseModel):
    account_number: int
    balance: float
    equity: float
    export_time: datetime
    day_profit: Optional[float] = 0.0
    day_equity: Optional[float] = 0.0
    strategy_name: Optional[str] = 'Default'

    class Config:
        from_attributes = True


class OpenPosition(BaseModel):
    account_number: int
    ticket: int
    open_time: Optional[datetime]
    size: float
    symbol: str
    type: str
    price: float
    tp_sl: Optional[float]
    profit: float

    class Config:
        from_attributes = True


class ClosedPosition(BaseModel):
    account_number: int
    ticket: int
    open_time: Optional[datetime]
    close_time: Optional[datetime]
    size: float
    symbol: str
    type: str
    price: float
    tp_sl: Optional[float]
    profit: float

    class Config:
        from_attributes = True


class DashboardData(BaseModel):
    accounts: List[Account]
    total_balance: float
    total_equity: float
    total_day_profit: float
    total_day_equity: float
    open_positions: List[OpenPosition]
    closed_positions: List[ClosedPosition]
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
