from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base


class User(Base):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(
        "first_name", nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        "last_name", nullable=False
    )
    email: Mapped[str] = mapped_column(
        "email", nullable=False
    )
    phone: Mapped[str] = mapped_column(
        "phone", nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        "hashed_password", nullable=False
    )

    def __repr__(self) -> str:
        return f"User(first_name={self.first_name},last_name={self.last_name},email={self.email},phone={self.phone})"
