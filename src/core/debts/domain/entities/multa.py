from dataclasses import Field, asdict, dataclass, field

from core.debts.domain.exceptions import EntityValidationException
from core.debts.domain.validators import MultaValidatorFactory, ValidatorInterface


@dataclass(kw_only=True, frozen=True, slots=True)
class Multa:
    amount: float
    auto_infraction: str
    description: str
    title: str = field(default="Infração de Trânsito")
    type: str = field(default="ticket")

    def __post_init__(self):
        self.validate()

    def to_dict(self):
        entity_dict = asdict(self)
        return entity_dict

    def validate(self):
        validator: ValidatorInterface = MultaValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        return cls.__dataclass_fields__[entity_field]  # pylint: disable=no-member
