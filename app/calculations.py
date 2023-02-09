def add(num1: int, num2: int):
    return num1 + num2

class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise InsufficientFunds('Insufficient funds in account')

    def collect_interest(self):
        self.balance *= 1.1

