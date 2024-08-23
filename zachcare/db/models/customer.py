from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from zachcare.db.models.base import Base


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    ssn: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    charges: Mapped[float] = mapped_column(default=0)
    policy_instance: Mapped["PolicyInstance"] = relationship(
        "PolicyInstance", back_populates="customer"
    )
    medical_history: Mapped["MedicalHistory"] = relationship(
        "MedicalHistory", back_populates="customer"
    )
