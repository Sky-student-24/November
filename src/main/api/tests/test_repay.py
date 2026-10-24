import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction

@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_positive(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account_credit(create_user_credit_request)

        credit_request = CreditRequest(
            accountId=response.id,
            amount=5000,
            termMonths=12
        )

        response_credit= api_manager.user_steps.credit(create_user_credit_request, credit_request)

        repay_request = RepayRequest(
            creditId=response_credit.creditId,
            accountId=response_credit.id,
            amount=response_credit.amount
        )

        repay_response = api_manager.user_steps.repay(create_user_credit_request, repay_request)

        assert repay_response.amountDeposited == repay_request.amount

        credit_from_db = Credit.get_credit_by_account_id(db_session, response.id)
        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)

        assert credit_from_db.balance == 0
        assert transaction_from_db.amount == 5000



    def test_credit_repay_negative(self, api_manager: ApiManager, create_user_credit_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account_credit(create_user_credit_request)

        credit_request = CreditRequest(
            accountId=response.id,
            amount=5000,
            termMonths=12
        )

        response_credit = api_manager.user_steps.credit(create_user_credit_request, credit_request)

        repay_request = RepayRequest(
            creditId=999,
            accountId=response_credit.id,
            amount=response_credit.amount
        )

        repay_response = api_manager.user_steps.repay_crash(create_user_credit_request, repay_request)

        repay_from_db = Credit.get_credit_by_account_id(db_session, repay_response)

        assert repay_from_db is None




