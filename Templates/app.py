import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import date, datetime, timedelta
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    def start(self):
        while True:
            print('''
            [1] -> Add subscription
            [2] -> Remove subscription
            [3] -> Total amount
            [4] -> Pay a subscription
            [5] -> Plot expenses in the last 12 months
            [6] -> Exit
            ''')

            choice = int(input('Choose an option: '))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.pay_subscription()
            elif choice == 5:
                self.subscription_service.plot_expenses_last_12_months()
            elif choice == 6:
                break

    def add_subscription(self):
        enterprise = input('Enterprise: ')
        site = input('Site: ')
        date_subscription = datetime.strptime(input('Date of subscription (MM/DD/YYYY): '), '%m/%d/%Y').date()
        value = Decimal(input('Value: '))
        
        subscription = Subscription(
            enterprise=enterprise,
            site=site,
            date_subscription=date_subscription,
            value=value
        )
        
        self.subscription_service.create(subscription)
        print('Subscription added successfully.')

    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Choose which subscription you want to delete')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.enterprise}')

        choice = int(input('Choose subscription: '))
        self.subscription_service.delete(choice)
        print('Subscription deleted successfully.')

    def total_value(self):
        total = self.subscription_service.total_value()
        print(f'Your total monthly subscription amount: {total:.2f}')

    def pay_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Choose which subscription you want to pay')

        for i in subscriptions:
            print(f'[{i.id}] -> {i.enterprise}')

        choice = int(input('Choose subscription: '))
        subscription = next(sub for sub in subscriptions if sub.id == choice)
        self.subscription_service.pay(subscription)
        print('Subscription paid successfully.')

if __name__ == '__main__':        
    UI().start()