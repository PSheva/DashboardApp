from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, DateTime
from datetime import datetime, time
from db import get_db, engine
import models
import schemas

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs (e.g., ['http://localhost:3000'])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

def fetch_unique_accounts_with_balance_and_equity(db: Session):
    subquery = db.query(
        models.AccountData.account_number,
        func.max(models.AccountData.export_time.cast(DateTime)).label("latest_export_time")
    ).group_by(models.AccountData.account_number).subquery()

    accounts_query = db.query(
        subquery.c.account_number,
        models.AccountData.balance,
        models.AccountData.equity,
        models.AccountData.export_time
    ).join(
        models.AccountData,
        (subquery.c.account_number == models.AccountData.account_number) & 
        (subquery.c.latest_export_time == models.AccountData.export_time.cast(DateTime))
    ).all()

    today_start = datetime.combine(datetime.today(), time.min)
    day_start_subquery = db.query(
        models.AccountData.account_number,
        func.min(models.AccountData.export_time.cast(DateTime)).label("start_export_time")
    ).filter(
        cast(models.AccountData.export_time, DateTime) >= today_start
    ).group_by(models.AccountData.account_number).subquery()

    day_start_query = db.query(
        day_start_subquery.c.account_number,
        models.AccountData.balance.label("day_start_balance"),
        models.AccountData.equity.label("day_start_equity")
    ).join(
        models.AccountData,
        (day_start_subquery.c.account_number == models.AccountData.account_number) & 
        (day_start_subquery.c.start_export_time == models.AccountData.export_time.cast(DateTime))
    ).all()

    day_start_map = {account: (balance, equity) for account, balance, equity in day_start_query}

    accounts = []
    for account_number, balance, equity, export_time in accounts_query:
        day_start_balance, day_start_equity = day_start_map.get(account_number, (balance, equity))
        day_profit = balance - day_start_balance
        day_equity = equity - day_start_equity
        accounts.append({
            "account_number": account_number,
            "balance": balance,
            "equity": equity,
            "day_profit": day_profit,
            "day_equity": day_equity,
            "export_time": export_time
        })

    last_export_time = max(account["export_time"] for account in accounts)
    accounts = [{"account_number": a["account_number"], "balance": a["balance"], "equity": a["equity"], "day_profit": a["day_profit"], "day_equity": a["day_equity"]} for a in accounts]
    
    return accounts, last_export_time

@app.get("/dashboard-data/", response_model=schemas.DashboardData)
async def get_dashboard_data(db: Session = Depends(get_db)):
    accounts, last_export_time = fetch_unique_accounts_with_balance_and_equity(db)
    
    total_balance = sum(account["balance"] for account in accounts)
    total_equity = sum(account["equity"] for account in accounts)
    total_day_profit = sum(account["day_profit"] for account in accounts)
    total_day_equity = sum(account["day_equity"] for account in accounts)
    
    dashboard_data = {
        "accounts": accounts,
        "total_balance": total_balance,
        "total_equity": total_equity,
        "total_day_profit": total_day_profit,
        "total_day_equity": total_day_equity,
        "last_export_time": last_export_time
    }
    
    return dashboard_data
