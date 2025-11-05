from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base


class File(Base):
    __tablename__ = "file"
    
    account_id: Mapped[UUID] = mapped_column(
        "account_uuid", nullable=False
    )
    file_name: Mapped[str] = mapped_column(
        "name", nullable=False, unique=True
    )
    file_path: Mapped[str] = mapped_column(
        "path", nullable=True
    )
    data_format: Mapped[str] = mapped_column(
        "format", nullable=True
    )

    def __repr__(self) -> str:
        return f"File(account_id={self.account_id},file_name={self.file_name},file_path={self.file_path},data_format={self.data_format})"
