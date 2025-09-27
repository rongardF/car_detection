from typing import Optional
from uuid import UUID
from pydantic import Field

from common.model import RequestBase, ResponseBase


class UserRequest(RequestBase):
    first_name: str = Field(title="First name", description="User first name", default="test")
    last_name: str = Field(title="Last name", description="User last name", default="user")
    email: str = Field(title="Email", description="User account email (must be unique)", default="test_user@email.eu")
    password: str = Field(title="Password", description="User account password", default="test_user")
    phone: Optional[str] = Field(title="Phone number", description="User account phone number (optional)", default="+372568966")


class UserResponse(ResponseBase):
    id: UUID = Field(title="User ID", description="Unique identifier for user account")
    first_name: str = Field(title="First name", description="User first name", default="test")
    last_name: str = Field(title="Last name", description="User last name", default="user")
    email: str = Field(title="Email", description="User account email (must be unique)", default="test_user@email.eu")
    phone: Optional[str] = Field(title="Phone number", description="User account phone number (optional)", default="+372568966")