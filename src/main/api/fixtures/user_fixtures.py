import pytest
from random_value_for_test import generate_credit, generate_term_months
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.create_user_request import CreateUserCreditRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest

@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_credit_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserCreditRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_user_account(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    user_response = api_manager.user_steps.create_account(user_request)
    account_id = user_response.id
    return user_request, account_id

@pytest.fixture
def user_transfer(api_manager):
    def _transfer(deposit_amount: float, transfer_amount: float):
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user_request)

        acc_from_response = api_manager.user_steps.create_account(user_request)
        acc_to_response = api_manager.user_steps.create_account(user_request)

        acc_from_id = acc_from_response.id
        acc_to_id = acc_to_response.id

        deposit_req = DepositRequest(accountId=acc_from_id, amount=deposit_amount)
        api_manager.user_steps.deposit(user_request, deposit_req)

        transfer_req = TransferRequest(
            fromAccountId=acc_from_id,
            toAccountId=acc_to_id,
            amount=transfer_amount,
        )

        return {
            "user_request": user_request,
            "acc_from_id": acc_from_id,
            "acc_to_id": acc_to_id,
            "deposit_amount": deposit_amount,
            "transfer_amount": transfer_amount,
            "transfer_request": transfer_req,
        }

    return _transfer

@pytest.fixture
def user_repay(api_manager, create_user_credit_request):
    response = api_manager.user_steps.create_account_credit(create_user_credit_request)
    account_id = response.id

    amount = generate_credit()
    term_months = generate_term_months()

    credit_request = CreditRequest(
        accountId=account_id,
        amount=amount,
        termMonths=term_months
    )

    credit_response = api_manager.user_steps.credit(create_user_credit_request, credit_request)

    assert credit_response is not None
    assert pytest.approx(credit_response.amount, rel=1e-6, abs=0.01) == amount

    yield {
        "account_id": account_id,
        "credit_id": credit_response.creditId,
        "amount": amount,
        "response": credit_response
    }