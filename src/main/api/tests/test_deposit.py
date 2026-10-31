import pytest
from sqlalchemy.orm import Session
from random_value_for_test import generate_deposit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestDeposit:
    def test_deposit_positive(self, api_manager: ApiManager, create_user_account, db_session: Session):
        amount = generate_deposit()
        user_request, account_id = create_user_account

        deposit_request = DepositRequest(accountId=account_id, amount=amount)

        response = api_manager.user_steps.deposit(user_request, deposit_request)

        assert response.balance != 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        transaction_from_db = Transaction.get_transaction_by_account_id(db_session, response.id)

        assert account_from_db.balance == amount
        assert account_from_db is not None, "Счёт не найден в БД"
        assert transaction_from_db.amount == amount
        assert transaction_from_db is not None, "Транзакция не найдена в БД"


    @pytest.mark.parametrize("amount", [500, 12000.0])
    def test_deposit_negative(self, api_manager: ApiManager, create_user_account, amount: float, db_session: Session):
        user_request, account_id = create_user_account

        deposit_request = DepositRequest(
            accountId=account_id,
            amount=amount
        )

        response = api_manager.user_steps.deposit_crash(user_request, deposit_request)

        deposit_from_db = Account.get_account_by_id(db_session, response)

        assert deposit_from_db is None