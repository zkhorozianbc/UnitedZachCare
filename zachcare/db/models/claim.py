from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from zachcare.db.models.base import Base
from typing import Literal, get_args

ClaimStatus = Literal["Submitted", "Rejected", "Settled"]

class Claim(Base):
    __tablename__ = "claim"
    id: Mapped[int] = mapped_column(primary_key=True)
    policy_instance = mapped_column(ForeignKey("policy_instance.id"))
    description: Mapped[str]
    status: Mapped[ClaimStatus] = mapped_column(Enum(
        *get_args(ClaimStatus),
        name="claim_enum",
        create_constraint=True,
        validate_strings=True,
    ))
    amt_settlement: Mapped[float]
