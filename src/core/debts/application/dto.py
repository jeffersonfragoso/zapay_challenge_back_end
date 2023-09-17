from dataclasses import dataclass
from typing import Dict, List, Optional

from core.debts.domain.entities import DPVAT, IPVA, Licenciamento, Multa


# Multa
@dataclass(kw_only=True, slots=True, frozen=True)
class MultaInput:
    amount: float
    auto_infraction: str
    description: str
    title: Optional[str] = Multa.get_field("title").default
    type: Optional[str] = Multa.get_field("type").default


@dataclass(kw_only=True, slots=True, frozen=True)
class MultaOutput:
    amount: float
    auto_infraction: str
    description: str
    title: str
    type: str


@dataclass(frozen=True, slots=True)
class MultaOutPutMapper:
    @classmethod
    def to_output(cls, multa: Multa) -> MultaOutput:
        return MultaOutput(
            amount=multa.amount,
            auto_infraction=multa.auto_infraction,
            description=multa.description,
            title=multa.title,
            type=multa.type,
        )


# IPVA
@dataclass(kw_only=True, slots=True, frozen=True)
class IPVAInput:
    amount: float
    description: Optional[str] = ""
    installment: Optional[str | int]
    title: Optional[str] = ""
    type: str = IPVA.get_field("type").default
    year: int


@dataclass(kw_only=True, slots=True, frozen=True)
class IPVAOutput:
    amount: float
    description: str
    installment: Optional[str | int]
    title: str
    type: str
    year: int


@dataclass(frozen=True, slots=True)
class IPVAOutPutMapper:
    @classmethod
    def to_output(cls, ipva: IPVA) -> IPVAOutput:
        output = IPVAOutput(
            amount=ipva.amount,
            description=ipva.description,
            installment=ipva.installment,
            title=ipva.title,
            type=ipva.type,
            year=ipva.year,
        )
        if output.installment is None:
            object.__delattr__(output, "installment")
        return output


# DPVAT
@dataclass(kw_only=True, slots=True, frozen=True)
class DPVATInput:
    amount: float
    description: str
    title: Optional[str] = DPVAT.get_field("title").default
    type: Optional[str] = DPVAT.get_field("type").default
    year: int


@dataclass(kw_only=True, slots=True, frozen=True)
class DPVATOutput:
    amount: float
    description: str
    title: str
    type: str
    year: int


@dataclass(frozen=True, slots=True)
class DPVATOutPutMapper:
    @classmethod
    def to_output(cls, dpvat: DPVAT) -> DPVATOutput:
        return DPVATOutput(
            amount=dpvat.amount,
            description=dpvat.description,
            title=dpvat.title,
            type=dpvat.type,
            year=dpvat.year,
        )


# Licenciamento
@dataclass(kw_only=True, slots=True, frozen=True)
class LicenciamentoInput:
    amount: float
    description: Optional[str]
    title: Optional[str] = Licenciamento.get_field("title").default
    type: Optional[str] = Licenciamento.get_field("type").default
    year: int


@dataclass(kw_only=True, slots=True, frozen=True)
class LicenciamentoOutput:
    amount: float
    description: str
    title: str
    type: str
    year: int


@dataclass(frozen=True, slots=True)
class LicenciamentoOutPutMapper:
    @classmethod
    def to_output(cls, licenciamento: Licenciamento) -> LicenciamentoOutput:
        return LicenciamentoOutput(
            amount=licenciamento.amount,
            description=licenciamento.description,
            title=licenciamento.title,
            type=licenciamento.type,
            year=licenciamento.year,
        )


# SPParse
@dataclass(slots=True, frozen=True)
class SPParserInput:
    data: dict


# SearchDebts
@dataclass(kw_only=True, slots=True, frozen=True)
class SearchDebtsInput:
    license_plate: str
    renavam: str
    debt_option: Optional[str] = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class SearchDebtsOutput:
    debts_list: List[Dict]


@dataclass(frozen=True)
class SearchDebtsOutputMapper:
    @classmethod
    def to_output(cls, collection: List[Dict] = []) -> SearchDebtsOutput:
        return SearchDebtsOutput(debts_list=collection)
