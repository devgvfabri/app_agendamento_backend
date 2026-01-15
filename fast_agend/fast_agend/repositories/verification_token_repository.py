from sqlalchemy.orm import Session
from fast_agend.models import VerificationToken


class VerificationTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, token: VerificationToken):
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def delete_by_user_and_type(self, user_id: int, type: str):
        self.db.query(VerificationToken).filter(
            VerificationToken.user_id == user_id,
            VerificationToken.type == type
        ).delete()
        self.db.commit()