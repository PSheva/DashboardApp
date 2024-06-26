from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text, DateTime
from datetime import datetime
from db import get_db, engine
import models
import schemas

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
models.Base.metadata.create_all(bind=engine)



def fetch_unique_accounts_with_balance_and_equity(db: Session):
    query = """
    WITH latest_records AS (
    SELECT
        ad.account_number,
        ad.balance,
        ad.equity,
        ad.export_time,
        ad.p_l,
        ai.strategy_name,
        ROW_NUMBER() OVER (PARTITION BY ad.account_number ORDER BY ad.export_time DESC) AS rn
    FROM account_data ad
    JOIN account_info ai ON ad.account_number = ai.account_number
),
filtered_latest_records AS (
    SELECT *
    FROM latest_records
    WHERE rn = 1
),
day_start_subquery AS (
    SELECT 
        account_number,
        MIN(CAST(export_time AS TIMESTAMP)) AS start_export_time
    FROM account_data
    WHERE CAST(export_time AS TIMESTAMP) >= DATE_TRUNC('day', CURRENT_DATE)
    GROUP BY account_number
),
day_start_records AS (
    SELECT
        day_start_subquery.account_number,
        account_data.balance AS day_start_balance,
        account_data.equity AS day_start_equity
    FROM day_start_subquery
    JOIN account_data ON day_start_subquery.account_number = account_data.account_number
    AND day_start_subquery.start_export_time = CAST(account_data.export_time AS TIMESTAMP)
),
previous_day_balance AS (
    SELECT
        ad.account_number,
        ad.balance AS prev_day_balance,
        ROW_NUMBER() OVER (PARTITION BY ad.account_number ORDER BY ad.export_time DESC) AS rn
    FROM account_data ad
    WHERE CAST(export_time AS TIMESTAMP) < DATE_TRUNC('day', CURRENT_DATE)
),
filtered_previous_day_balance AS (
    SELECT
        account_number,
        prev_day_balance
    FROM previous_day_balance
    WHERE rn = 1
),
week_start_subquery AS (
    SELECT 
        account_number,
        MIN(CAST(export_time AS TIMESTAMP)) AS start_export_time
    FROM account_data
    WHERE CAST(export_time AS TIMESTAMP) >= DATE_TRUNC('week', CURRENT_DATE)
    GROUP BY account_number
),
week_start_records AS (
    SELECT
        week_start_subquery.account_number,
        account_data.balance AS week_start_balance,
        account_data.equity AS week_start_equity
    FROM week_start_subquery
    JOIN account_data ON week_start_subquery.account_number = account_data.account_number
    AND week_start_subquery.start_export_time = CAST(account_data.export_time AS TIMESTAMP)
),
previous_week_balance AS (
    SELECT
        ad.account_number,
        ad.balance AS prev_week_balance,
        ROW_NUMBER() OVER (PARTITION BY ad.account_number ORDER BY ad.export_time DESC) AS rn
    FROM account_data ad
    WHERE CAST(export_time AS TIMESTAMP) < DATE_TRUNC('week', CURRENT_DATE)
),
filtered_previous_week_balance AS (
    SELECT
        account_number,
        prev_week_balance
    FROM previous_week_balance
    WHERE rn = 1
),
month_start_subquery AS (
    SELECT 
        account_number,
        MIN(CAST(export_time AS TIMESTAMP)) AS start_export_time
    FROM account_data
    WHERE CAST(export_time AS TIMESTAMP) >= DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY account_number
),
month_start_records AS (
    SELECT
        month_start_subquery.account_number,
        account_data.balance AS month_start_balance,
        account_data.equity AS month_start_equity
    FROM month_start_subquery
    JOIN account_data ON month_start_subquery.account_number = account_data.account_number
    AND month_start_subquery.start_export_time = CAST(account_data.export_time AS TIMESTAMP)
),
previous_month_balance AS (
    SELECT
        ad.account_number,
        ad.balance AS prev_month_balance,
        ROW_NUMBER() OVER (PARTITION BY ad.account_number ORDER BY ad.export_time DESC) AS rn
    FROM account_data ad
    WHERE CAST(export_time AS TIMESTAMP) < DATE_TRUNC('month', CURRENT_DATE)
),
filtered_previous_month_balance AS (
    SELECT
        account_number,
        prev_month_balance
    FROM previous_month_balance
    WHERE rn = 1
),
deposits_by_day AS (
    SELECT
        account_number,
        SUM(profit) AS day_deposits
    FROM balance_ops
    WHERE CAST(export_time AS TIMESTAMP) >= DATE_TRUNC('day', CURRENT_DATE)
    GROUP BY account_number
),
deposits_by_week AS (
    SELECT
        account_number,
        SUM(profit) AS week_deposits
    FROM balance_ops
    WHERE CAST(export_time AS TIMESTAMP) >= DATE_TRUNC('week', CURRENT_DATE)
    GROUP BY account_number
),
deposits_by_month AS (
    SELECT
        account_number,
        SUM(profit) AS month_deposits
    FROM balance_ops
    WHERE CAST(export_time AS TIMESTAMP) >= DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY account_number
),
final_results AS (
    SELECT DISTINCT ON (flr.account_number)
        flr.account_number,
        flr.balance,
        flr.equity,
        flr.export_time,
        flr.strategy_name,
        COALESCE(flr.balance - COALESCE(dsr.day_start_balance, fpdb.prev_day_balance), flr.balance) - COALESCE(dbd.day_deposits, 0) AS day_profit,
        COALESCE(flr.balance - COALESCE(wsr.week_start_balance, fpwb.prev_week_balance), flr.balance) - COALESCE(dbw.week_deposits, 0) AS week_profit,
        COALESCE(flr.balance - COALESCE(msr.month_start_balance, fpmb.prev_month_balance), flr.balance) - COALESCE(dbm.month_deposits, 0) AS month_profit,
        flr.p_l AS day_equity,
        CASE WHEN dsr.day_start_balance IS NULL THEN 'Using previous day balance' ELSE NULL END AS message
    FROM filtered_latest_records flr
    LEFT JOIN day_start_records dsr ON flr.account_number = dsr.account_number
    LEFT JOIN filtered_previous_day_balance fpdb ON flr.account_number = fpdb.account_number
    LEFT JOIN week_start_records wsr ON flr.account_number = wsr.account_number
    LEFT JOIN filtered_previous_week_balance fpwb ON flr.account_number = fpwb.account_number
    LEFT JOIN month_start_records msr ON flr.account_number = msr.account_number
    LEFT JOIN filtered_previous_month_balance fpmb ON flr.account_number = fpmb.account_number
    LEFT JOIN deposits_by_day dbd ON flr.account_number = dbd.account_number
    LEFT JOIN deposits_by_week dbw ON flr.account_number = dbw.account_number
    LEFT JOIN deposits_by_month dbm ON flr.account_number = dbm.account_number
    ORDER BY flr.account_number, flr.export_time DESC
)
SELECT * FROM final_results;



    """

    result = db.execute(text(query))

    accounts = []
    for row in result:
        accounts.append({
            "account_number": row[0],
            "balance": row[1],
            "equity": row[2],
            "export_time": row[3],
            "strategy_name": row[4],
            "day_profit": row[5],
            "week_profit": row[6],  # New line for week profit
            "month_profit": row[7],  # New line for month profit
            "day_equity": row[8],
            "message": row[9]  # New line to capture the message
        })

    return accounts



def fetch_open_positions(db: Session):
    subquery = (
        db.query(
            models.TradeData.ticket,
            func.max(models.TradeData.export_time).label('latest_export_time')
        )
        .group_by(models.TradeData.ticket)
        .subquery()
    )

    open_positions_query = (
        db.query(
            models.TradeData.account_number,
            models.TradeData.ticket,
            models.TradeData.open_time,
            models.TradeData.close_time,
            models.TradeData.lots.label("size"),
            models.TradeData.symbol,
            models.TradeData.type,
            models.TradeData.open_price.label("price"),
            models.TradeData.take_profit.label("tp_sl"),
            models.TradeData.profit,
        )
        .join(
            subquery,
            (models.TradeData.ticket == subquery.c.ticket)
            & (models.TradeData.export_time == subquery.c.latest_export_time)
        )
        .filter(models.TradeData.close_time.is_(None))
        .filter(models.TradeData.type != 'Balance')
        .order_by(models.TradeData.export_time.desc())
        .limit(150)
        .all()
    )

    return open_positions_query


def fetch_closed_positions(db: Session):
    closed_positions_query = db.query(
        models.TradeData.account_number,
        models.TradeData.ticket,
        models.TradeData.open_time,
        models.TradeData.close_time,
        models.TradeData.lots.label("size"),
        models.TradeData.symbol,
        models.TradeData.type,
        models.TradeData.close_price.label("price"),
        models.TradeData.take_profit.label("tp_sl"),
        models.TradeData.profit
    ).filter(
        models.TradeData.close_time.isnot(None)
    ).order_by(
        models.TradeData.export_time.desc()
    ).limit(150).all()

    return closed_positions_query


@app.get("/", response_model=schemas.DashboardData)
async def get_dashboard_data(db: Session = Depends(get_db)):
    accounts = fetch_unique_accounts_with_balance_and_equity(db)
    open_positions = fetch_open_positions(db) or []
    closed_positions = fetch_closed_positions(db) or []

    total_balance = sum(account["balance"] for account in accounts)
    total_equity = sum(account["equity"] for account in accounts)
    total_day_profit = sum(account["day_profit"] for account in accounts)
    total_day_equity = sum(account["day_equity"] for account in accounts)
    total_week_profit = sum(account["week_profit"] for account in accounts)
    total_month_profit = sum(account["month_profit"] for account in accounts) 
    last_export_time = accounts[0]["export_time"] if accounts else None

    dashboard_data = {
        "accounts": accounts,
        "total_balance": total_balance,
        "total_equity": total_equity,
        "total_day_profit": total_day_profit,
        "total_day_equity": total_day_equity,
        "total_week_profit": total_week_profit,
        "total_month_profit": total_month_profit,
        "open_positions": open_positions,
        "closed_positions": closed_positions,
        "last_export_time": last_export_time
    }

    return dashboard_data
