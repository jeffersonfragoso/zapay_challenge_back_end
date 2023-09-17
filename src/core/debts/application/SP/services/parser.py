from dataclasses import dataclass
from typing import Generator, List

from core.debts.application.dto import (
    DPVATInput,
    DPVATOutput,
    IPVAInput,
    IPVAOutput,
    LicenciamentoInput,
    LicenciamentoOutput,
    MultaInput,
    MultaOutput,
    SPParserInput,
)
from core.debts.application.use_cases import (
    CreateDPVATUseCase,
    CreateIPVAUseCase,
    CreateLicenciamentoUseCase,
    CreateMultaUseCase,
)


@dataclass(kw_only=True, slots=True, frozen=True)
class SPParser:
    use_case_create_IPVA: CreateIPVAUseCase
    use_case_create_multa: CreateMultaUseCase
    use_case_create_DPVAT: CreateDPVATUseCase
    use_case_create_licenciamento: CreateLicenciamentoUseCase

    def collect_ipva_debts(
        self, input_param: SPParserInput
    ) -> Generator[IPVAOutput, None, None]:
        """
        Formatar os dados de IPVA.
        """

        debts = self._get_debts_from_json(input_param.data, "IPVAs")

        if debts is None:
            return []
        else:
            debts = debts["IPVA"]

        for debt in debts:
            ipva_input_param = IPVAInput(
                amount=debt.get("Valor"),
                installment=debt.get("Cota", None),
                year=debt.get("Exercicio"),
            )
            yield self.use_case_create_IPVA.execute(ipva_input_param)

    def collect_ticket_debts(
        self, input_param: SPParserInput
    ) -> Generator[MultaOutput, None, None]:
        """
        Formatar os dados de Multas.
        """

        debts = self._get_debts_from_json(input_param.data, "Multas")

        if debts is None:
            return []
        else:
            debts = debts["Multa"]

        for debt in debts:
            multa_input_param = MultaInput(
                amount=debt.get("Valor"),
                auto_infraction=debt.get("AIIP"),
                description=debt.get("DescricaoEnquadramento"),
            )
            yield self.use_case_create_multa.execute(multa_input_param)

    def collect_insurance_debts(
        self, input_param: SPParserInput
    ) -> Generator[DPVATOutput, None, None]:
        """
        Formatar os dados de DPVAT.
        """

        debts = self._get_debts_from_json(input_param.data, "DPVATs")

        if debts is None:
            return []
        else:
            debts = debts["DPVAT"]

        for debt in debts:
            dpvat_input_param = DPVATInput(
                amount=debt.get("Valor"),
                description=debt.get("DescricaoServico", None),
                year=debt.get("Exercicio"),
            )
            yield self.use_case_create_DPVAT.execute(dpvat_input_param)

    def collect_licensing_debts(
        self, input_param: SPParserInput
    ) -> Generator[LicenciamentoOutput, None, None]:
        """
        Formatar os dados de Licenciamento.
        """

        debt = self._get_debts_from_json(input_param.data, "Licenciamento")

        if not debt:
            return []

        licancimento_input_param = LicenciamentoInput(
            amount=debt.get("TaxaLicenciamento"),
            description=debt.get("DescricaoLicenciamento", None),
            year=debt.get("Exercicio"),
        )
        yield self.use_case_create_licenciamento.execute(licancimento_input_param)

    def collect_all_debts(self, input_param: SPParserInput) -> List[object]:
        """
        Formatar os dados de todos as categorias de debitos.
        """
        multas = list(self.collect_ticket_debts(input_param))
        ipvas = list(self.collect_ipva_debts(input_param))
        dpvats = list(self.collect_insurance_debts(input_param))
        licenciamento = list(self.collect_licensing_debts(input_param))

        return multas + ipvas + dpvats + licenciamento

    def _get_debts_from_json(self, data, category):
        """
        Retorna a categoria especifica da pesquisa.
        """

        try:
            return data[category]

        except KeyError:
            return None
