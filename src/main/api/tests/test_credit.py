import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_positive(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account_credit(create_user_credit_request)

        credit_request = CreditRequest(
            accountId=response.id,
            amount=5000,
            termMonths=12
        )

        credit_response = api_manager.user_steps.credit(create_user_credit_request, credit_request)

        assert credit_response.amount == 5000, "Сумма кредита не совпадает"
        assert credit_response.balance >= 5000

        credit_from_db = Credit.get_credit_by_account_id(db_session, response.id)
        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)


        assert credit_from_db.balance == -5000
        assert transaction_from_db.amount == 5000


    def test_credit_request_negative(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account(create_user_request)

        credit_request = CreditRequest(
            accountId=response.id,
            amount=5000,
            termMonths=12
        )

        response = api_manager.user_steps.credit_crash(create_user_request, credit_request)

        credit_from_db = Credit.get_credit_by_account_id(db_session, response)

        assert credit_from_db is None








