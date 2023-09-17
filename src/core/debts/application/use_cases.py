from dataclasses import asdict, dataclass

from core.debts.application.dto import (
    DPVATInput,
    DPVATOutput,
    DPVATOutPutMapper,
    IPVAInput,
    IPVAOutput,
    IPVAOutPutMapper,
    LicenciamentoInput,
    LicenciamentoOutput,
    LicenciamentoOutPutMapper,
    MultaInput,
    MultaOutput,
    MultaOutPutMapper,
)
from core.debts.domain.entities import DPVAT, IPVA, Licenciamento, Multa


@dataclass(slots=True, frozen=True)
class CreateMultaUseCase:
    def execute(self, input_param: MultaInput) -> MultaOutput:
        multa = Multa(**asdict(input_param))
        return MultaOutPutMapper.to_output(multa)


@dataclass(slots=True, frozen=True)
class CreateIPVAUseCase:
    def execute(self, input_param: IPVAInput) -> IPVAOutput:
        # cria entidade de dominio
        ipva = IPVA(**asdict(input_param))

        # aplica regras de negócio
        ipva.build_title()
        ipva.set_description()
        ipva.set_installment()

        # retorna um output conforme necessidade do caso de uso
        return IPVAOutPutMapper.to_output(ipva)


@dataclass(slots=True, frozen=True)
class CreateDPVATUseCase:
    def execute(self, input_param: DPVATInput) -> DPVATOutput:
        dpvat = DPVAT(**asdict(input_param))

        dpvat.amount_to_float()
        dpvat.build_description()

        return DPVATOutPutMapper.to_output(dpvat)


@dataclass(slots=True, frozen=True)
class CreateLicenciamentoUseCase:
    def execute(self, input_param: LicenciamentoInput) -> LicenciamentoOutput:
        licenciamento = Licenciamento(**asdict(input_param))

        licenciamento.amount_to_float()
        licenciamento.build_description()

        return LicenciamentoOutPutMapper.to_output(licenciamento)
