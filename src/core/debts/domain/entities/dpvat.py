from dataclasses import Field, asdict, dataclass, field
from typing import Any, Optional

from core.debts.domain.exceptions import EntityValidationException
from core.debts.domain.validators import DPVATValidatorFactory, ValidatorInterface


@dataclass(kw_only=True, frozen=True, slots=True)
class DPVAT:
    amount: float
    description: Optional[str]
    title: str = field(default="Seguro Obrigatório")
    type: str = field(default="insurance")
    year: int

    def __post_init__(self):
        self.validate()

    def to_dict(self):
        entity_dict = asdict(self)
        return entity_dict

    def validate(self):
        validator: ValidatorInterface = DPVATValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)

    def amount_to_float(self):
        self._set("amount", (self.amount / 100))

    def build_description(self):
        if not self.description:
            self._set("description", f"DPVAT {self.year}")

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        return cls.__dataclass_fields__[entity_field]  # pylint: disable=no-member

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
        return self
