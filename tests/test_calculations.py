import pytest
from app.calculations import add, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize('num1, num2, expected_value', [
    (3, 5, 8),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected_value):
     assert add(num1, num2) == expected_value

def test_bank_set_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100

def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 150

def test_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 50

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 110

@pytest.mark.parametrize('deposited, withdrew, expected_value', [
    (100, 50, 165),
    (10, 10, 110),
    (1000, 200, 990)
])
def test_bank_transaction(bank_account, deposited, withdrew, expected_value):
    bank_account.deposit(deposited)
    bank_account.withdraw(withdrew)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == expected_value

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(100)