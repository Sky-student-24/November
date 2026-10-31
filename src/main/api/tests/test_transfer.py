import pytest
from sqlalchemy.orm import Session
from random_value_for_test import generate_deposit_transfer
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransfer:
    def test_transfer_positive(self, api_manager: ApiManager, user_transfer, db_session: Session):
        deposit_amount, transfer_amount = generate_deposit_transfer()

        data = user_transfer(deposit_amount=deposit_amount, transfer_amount=transfer_amount)

        response = api_manager.user_steps.transfer(data["user_request"], data["transfer_request"])

        assert response is not None

        acc_from = Account.get_account_by_id(db_session, data["acc_from_id"])
        acc_to = Account.get_account_by_id(db_session, data["acc_to_id"])

        assert acc_from.balance == pytest.approx(deposit_amount - transfer_amount, rel=1e-6, abs=0.01)
        assert acc_to.balance == pytest.approx(transfer_amount, rel=1e-6, abs=0.01)

    @pytest.mark.parametrize("deposit_amount,transfer_amount", [
        (5000.0, 7000.0),
    ])
    def test_transfer_negative(self, api_manager: ApiManager, user_transfer, deposit_amount, transfer_amount,db_session: Session):

        data = user_transfer(deposit_amount=deposit_amount, transfer_amount=transfer_amount)

        response = api_manager.user_steps.transfer_crash(data["user_request"], data["transfer_request"])

        assert response is None

        acc_from = Account.get_account_by_id(db_session, data["acc_from_id"])
        acc_to = Account.get_account_by_id(db_session, data["acc_to_id"])

        assert acc_from is not None
        assert acc_to is not None

        assert pytest.approx(acc_from.balance, rel=1e-6, abs=0.01) == deposit_amount
        assert pytest.approx(acc_to.balance, rel=1e-6, abs=0.01) == 0.0