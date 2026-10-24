import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestDeposit:
    def test_deposit_positive(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        user_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=user_response.id,
            amount=5000
        )

        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        assert response.balance != 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)

        assert account_from_db.balance == 5000
        assert transaction_from_db.amount == 5000


    def test_deposit_negative(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        user_response = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=user_response.id,
            amount=12000
        )

        response = api_manager.user_steps.deposit_crash(create_user_request, deposit_request)

        deposit_from_db = Account.get_account_by_id(db_session, response)

        assert deposit_from_db is None







