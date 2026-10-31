import pytest
from sqlalchemy.orm import Session
from random_value_for_test import generate_credit, generate_term_months
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest, CreateUserCreditRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_positive(self, api_manager: ApiManager, create_user_credit_request: CreateUserCreditRequest, db_session: Session):
        amount = generate_credit()
        termMonths = generate_term_months()

        response = api_manager.user_steps.create_account_credit(create_user_credit_request)

        credit_request = CreditRequest(
            accountId=response.id,
            amount=amount,
            termMonths=termMonths
        )

        credit_response = api_manager.user_steps.credit(create_user_credit_request, credit_request)

        assert pytest.approx(credit_response.amount, rel=1e-6, abs=0.01) == amount
        assert credit_response.balance >= amount - 0.01

        credit_from_db = Credit.get_credit_by_account_id(db_session, response.id)
        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)

        assert pytest.approx(credit_from_db.balance, rel=1e-6, abs=0.01) == -amount
        assert pytest.approx(transaction_from_db.amount, rel=1e-6, abs=0.01) == amount


    def test_credit_request_negative(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        amount = generate_credit()
        termMonths = generate_term_months()

        response = api_manager.user_steps.create_account_credit(create_user_request)

        credit_request = CreditRequest(
            accountId=response.id,
            amount=amount,
            termMonths=termMonths
        )

        credit_response = api_manager.user_steps.credit_crash(create_user_request, credit_request)

        assert credit_response is None

        account_from_db = Account.get_account_by_id(db_session, response.id)
        credit_from_db = Credit.get_credit_by_account_id(db_session, response.id)
        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)

        assert credit_from_db is None
        assert transaction_from_db is None
        assert account_from_db.balance == 0.0, "Баланс не должен измениться при отказе в кредите"







