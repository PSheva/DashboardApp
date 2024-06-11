from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Account(BaseModel):
    account_number: int
    balance: float
    equity: Optional[float]
    day_profit: Optional[float]
    day_equity: Optional[float]

class Ticket(BaseModel):
    ticket: float

class TicketList(BaseModel):
    number_of_tickets: int
    tickets: List[Ticket]

class TicketSummary(BaseModel):
    number_of_tickets: int
    total_value: Optional[float] = None  # Assuming total_value is optional

class DashboardData(BaseModel):
    accounts: List[Account]
    ticket_summary: Optional[TicketSummary] = None  # Optional field
    tickets: Optional[TicketList] = None  # Optional field
    total_balance: float
    total_equity: Optional[float]
    total_day_profit: Optional[float]
    total_day_equity: Optional[float]
    last_export_time: datetime  # Include last export time in the schema
