from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from zachcare.db.models.base import Base
from typing import Literal, get_args
PolicyName = Literal["HMO","PPO"]

class Policy(Base):
    __tablename__ = "policy"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[PolicyName] = mapped_column(
        Enum(
            *get_args(PolicyName),
            name="policy_name_enum",
            create_constraint=True,
            validate_string=True,
        )
    )
    policy_instances: Mapped["PolicyInstance"] = relationship('PolicyInstance', back_populates='policy')

class PolicyInstance(Base):
    __tablename__ = "policy_instance"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    policy_id: Mapped[int] = mapped_column(ForeignKey("policy.id"))
    premium: Mapped[int]
    customer: Mapped['Customer'] = relationship('Customer', back_populates='policy_instance')
    policy: Mapped["Policy"] = relationship('Policy', back_populates='policy_instances')
