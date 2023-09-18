from dataclasses import Field, asdict, dataclass, field
from typing import Any, Optional

from core.debts.domain.exceptions import EntityValidationException
from core.debts.domain.validators import IPVAValidatorFactory, ValidatorInterface


@dataclass(kw_only=True, frozen=True, slots=True)
class IPVA:
    amount: float
    description: str
    installment: Optional[str | int]
    title: str
    type: str = field(default="ipva")
    year: int

    def __post_init__(self):
        self.validate()

    def to_dict(self):
        entity_dict = asdict(self)
        return entity_dict

    def validate(self):
        validator: ValidatorInterface = IPVAValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)

    def build_title(self):
        value_cota = "Única" if self.installment in [7, 8, 0] else self.installment
        builded_title = f"IPVA - Cota {value_cota}"
        self._set("title", builded_title)

    def amount_to_float(self):
        self._set("amount", (self.amount / 100))

    def set_description(self):
        self._set("description", f"IPVA {self.year}")

    def set_installment(self):
        if _ := bool(self.installment in [0, 7, 8]):
            self._set("installment", "unique")

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        return cls.__dataclass_fields__[entity_field]  # pylint: disable=no-member

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
        return self
