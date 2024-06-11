

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import Null, func
from db import get_db, engine
import models
import schemas

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/accounts/", response_model=list[int])
async def read_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    accounts = db.query(models.CurrentDataFrame.account_number).offset(skip).limit(limit).all()
    return [account[0] for account in accounts]


@app.get("/tickets-summary/", response_model=schemas.TicketList)
async def tickets_summary(db: Session = Depends(get_db)):
    result = db.query(
        func.count(models.CurrentDataFrame.ticket).label('number_of_tickets'),
        
    ).first()
   
    return {
       
        "number_of_tickets": result.number_of_tickets,
       "tickets": [] # Returning an empty list for tickets as this endpoint does not provide tickets
    }


@app.get("/tickets/", response_model=schemas.TicketList)
async def get_tickets(db: Session = Depends(get_db)):
    tickets_query = db.query(
        models.CurrentDataFrame.ticket
    ).filter(
        models.CurrentDataFrame.ticket.isnot(None)
    ).distinct().all()
    
    # Correctly format tickets
    tickets = [{"ticket": ticket} for (ticket,) in tickets_query]
    number_of_tickets = len(tickets)
    
    return {"number_of_tickets": number_of_tickets, "tickets": tickets}
