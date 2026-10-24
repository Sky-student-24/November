import pytest
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransfer:
    def test_transfer_positive(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        acc_1 = api_manager.user_steps.create_account(create_user_request)
        acc_2 = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
            accountId=acc_1.id,
            amount=5000
        )

        api_manager.user_steps.deposit(create_user_request, deposit_request)

        transfer_request = TransferRequest(
            fromAccountId=acc_1.id,
            toAccountId=acc_2.id,
            amount=2000
        )

        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert response.fromAccountIdBalance != 0

        acc_from = Account.get_account_by_id(db_session, acc_1.id)
        acc_to = Account.get_account_by_id(db_session, acc_2.id)

        assert acc_from.balance == 3000
        assert acc_to.balance == 2000


    def test_transfer_negative(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        acc_1 = api_manager.user_steps.create_account(create_user_request)
        acc_2 = api_manager.user_steps.create_account(create_user_request)

        deposit_request = DepositRequest(
        accountId = acc_1.id,
        amount = 5000

        )

        api_manager.user_steps.deposit(create_user_request, deposit_request)

        transfer_request = TransferRequest(
        fromAccountId = acc_1.id,
        toAccountId = acc_2.id,
        amount = 7000

        )

        api_manager.user_steps.transfer_crash(create_user_request, transfer_request)


        acc_from = Account.get_account_by_id(db_session, acc_1.id)
        acc_to = Account.get_account_by_id(db_session, acc_2.id)

        assert abs(acc_from.balance - 5000.0) < 0.01, "Баланс отправителя был изменен"
        assert abs(acc_to.balance - 0.0) < 0.01, "Баланс получателя был изменен"
