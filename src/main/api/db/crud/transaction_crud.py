from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction



class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_account_id(db: Session, account_id: int):
        return db.query(Transaction).filter_by(to_account_id=account_id).first()