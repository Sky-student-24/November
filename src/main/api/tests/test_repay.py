import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest, CreateUserCreditRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction

@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_positive(self, api_manager: ApiManager, user_repay, create_user_credit_request: CreateUserCreditRequest, db_session: Session):
        data = user_repay

        repay_request = RepayRequest(
            creditId=data["credit_id"],
            accountId=data["account_id"],
            amount=data["amount"]
        )

        repay_response = api_manager.user_steps.repay(create_user_credit_request=create_user_credit_request, repay_request=repay_request)

        assert repay_response is not None
        assert pytest.approx(repay_response.amountDeposited, rel=1e-6, abs=0.01) == data["amount"]


        credit_from_db = Credit.get_credit_by_account_id(db_session, data["account_id"])
        assert credit_from_db is not None
        assert pytest.approx(credit_from_db.balance, rel=1e-6, abs=0.01) == 0.0


        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, data["account_id"])
        assert transaction_from_db is not None
        assert pytest.approx(transaction_from_db.amount, rel=1e-6, abs=0.01) == data["amount"]



    def test_credit_repay_negative(self, api_manager: ApiManager, user_repay, create_user_credit_request: CreateUserCreditRequest, db_session: Session):
        data = user_repay

        partial_amount = data["amount"] / 2

        repay_request = RepayRequest(
            creditId=data["credit_id"],
            accountId=data["account_id"],
            amount=partial_amount
        )

        repay_response = api_manager.user_steps.repay_crash(create_user_credit_request=create_user_credit_request, repay_request=repay_request)
        assert repay_response is None

        credit_from_db = Credit.get_credit_by_account_id(db_session, data["account_id"])
        assert pytest.approx(credit_from_db.balance, rel=1e-6, abs=0.01) == -data["amount"]
