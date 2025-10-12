from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base


class APIKey(Base):
    __tablename__ = "api_key"

    account_id: Mapped[UUID] = mapped_column(
        "account_id", ForeignKey("account.uuid", ondelete="CASCADE"), nullable=False
    )
    encrypted_key: Mapped[bytes] = mapped_column(
        "key", nullable=False
    )
    hashed_key: Mapped[str] = mapped_column(
        "hashed_key", nullable=False
    )

    def __repr__(self) -> str:
        return f"APIKey(account_id={self.account_id},hashed_key={self.hashed_key},encrypted_key={self.encrypted_key})"
