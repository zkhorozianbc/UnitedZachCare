from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from zachcare.db.models.base import Base
from typing import Literal, get_args


class MedicalCondition(Base):
    __tablename__ = "medical_condition"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    medical_history: Mapped["MedicalHistory"] = relationship(
        "MedicalHistory",
        back_populates="medical_condition",
        foreign_keys="[MedicalHistory.medical_condition_id]",
    )
    family_medical_history: Mapped["MedicalHistory"] = relationship(
        "MedicalHistory",
        back_populates="family_medical_condition",
        foreign_keys="[MedicalHistory.family_medical_condition_id]",
    )


ExcerciseFrequency = Literal["Never", "Occasionally", "Rarely", "Frequently"]
Gender = Literal["male", "female"]


class MedicalHistory(Base):
    __tablename__ = "medical_history"
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id"), primary_key=True
    )
    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="medical_history"
    )

    age: Mapped[int]
    gender: Mapped[Gender] = mapped_column(
        Enum(
            *get_args(Gender),
            name="gender_enum",
            create_constraint=True,
            validate_string=True,
        )
    )
    bmi: Mapped[float]
    children: Mapped[int]
    is_smoker: Mapped[bool]
    region: Mapped[str]
    exercise_frequency: Mapped[ExcerciseFrequency] = mapped_column(
        Enum(
            *get_args(ExcerciseFrequency),
            name="excercise_frequency_enum",
            create_constraint=True,
            validate_strings=True,
        )
    )
    occupation: Mapped[str | None]
    medical_condition_id: Mapped[int | None] = mapped_column(
        ForeignKey("medical_condition.id")
    )
    family_medical_condition_id: Mapped[int | None] = mapped_column(
        ForeignKey("medical_condition.id")
    )

    medical_condition: Mapped[MedicalCondition] = relationship(
        "MedicalCondition",
        back_populates="medical_history",
        foreign_keys=[medical_condition_id],
    )
    family_medical_condition: Mapped[MedicalCondition] = relationship(
        "MedicalCondition",
        back_populates="family_medical_history",
        foreign_keys=[family_medical_condition_id],
    )
