import random


def generate_deposit():
        return round(random.uniform(1000.0, 9000.0), 2)

def generate_deposit_transfer():
    deposit = round(random.uniform(1000.0, 9000.0), 2)
    transfer = round(deposit * random.uniform(0.1, 0.9), 2)
    return deposit, transfer

def generate_credit():
    return round(random.uniform(5000.0, 15000.0), 2)

def generate_term_months() -> int:
    return random.randint(1, 60)
