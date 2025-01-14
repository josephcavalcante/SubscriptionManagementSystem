from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True):
    id: int = Field(primary_key=True)
    enterprise: str
    site: Optional[str] = None
    date_subscription: date
    value: Decimal
    
class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    id_subscription: int = Field(foreign_key="subscription.id")
    subscription: Subscription = Relationship()
    date_payment: date
    active: bool = Field(default=True)