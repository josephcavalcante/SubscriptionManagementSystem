import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription
        
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            return results
        
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            subscription = session.exec(statement).one()   
            payment_statement = select(Payments).where(Payments.id_subscription == id)
            payments = session.exec(payment_statement).all()
            for payment in payments:
                payment.active = False  
                session.add(payment)
            session.delete(subscription)
            session.commit()
        
    def _has_pay(self, results):
        for result in results:
            if result.date_payment.month == date.today().month:
                return True
        return False
            
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.enterprise == subscription.enterprise)
            results = session.exec(statement).all()
          
            if self._has_pay(results):
                question = input('You have already paid this month, do you want to pay again? (yes/no): ')
                
                if not question.upper() == 'YES':
                    return
            pay = Payments(id_subscription=subscription.id, date_payment=date.today()) 
            session.add(pay)
            session.commit()
    
    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            total = sum(subscription.value for subscription in results)
            return total
        
    def plot_expenses_last_12_months(self):
        with Session(self.engine) as session:
            one_year_ago = date.today() - timedelta(days=365)
            statement = select(Payments).where(Payments.date_payment >= one_year_ago, Payments.active == True)
            results = session.exec(statement).all()
            
            months = [date.today() - timedelta(days=30 * i) for i in range(12)]
            months.reverse()
            expenses = [0] * 12
            
            for payment in results:
                month_index = (date.today().year - payment.date_payment.year) * 12 + date.today().month - payment.date_payment.month
                if month_index < 12:
                    expenses[11 - month_index] += payment.subscription.value
            
            plt.figure(figsize=(10, 6))
            plt.plot([month.strftime('%b %Y') for month in months], expenses, marker='o')
            plt.xlabel('Month')
            plt.ylabel('Expenses')
            plt.title('Expenses in the Last 12 Months')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()