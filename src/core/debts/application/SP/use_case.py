from dataclasses import asdict, dataclass
from typing import Dict, Generator

from core.debts.application.dto import (
    SearchDebtsInput,
    SearchDebtsOutput,
    SearchDebtsOutputMapper,
    SPParserInput,
)
from core.debts.application.SP.services import SPParser, SPService


@dataclass(kw_only=True, frozen=True, slots=True)
class SearchcDebtsUseCase:
    service_detran_SP: SPService
    service_parser_SP: SPParser

    def execute(
        self, input_param: SearchDebtsInput
    ) -> Generator[SearchDebtsOutput, None, None]:
        try:
            response: Dict = self.service_detran_SP.execute(**asdict(input_param))
            parser_input_param = SPParserInput(data=response)

            match input_param.debt_option:
                case "":
                    yield SearchDebtsOutputMapper.to_output(
                        self.service_parser_SP.collect_all_debts(parser_input_param)
                    )
                case "ticket":
                    yield SearchDebtsOutputMapper.to_output(
                        list(
                            self.service_parser_SP.collect_ticket_debts(
                                parser_input_param
                            )
                        )
                    )
                case "ipva":
                    yield SearchDebtsOutputMapper.to_output(
                        list(
                            self.service_parser_SP.collect_ipva_debts(
                                parser_input_param
                            )
                        )
                    )
                case "dpvat":
                    yield SearchDebtsOutputMapper.to_output(
                        list(
                            self.service_parser_SP.collect_insurance_debts(
                                parser_input_param
                            )
                        )
                    )
                case "licensing":
                    yield SearchDebtsOutputMapper.to_output(
                        list(
                            self.service_parser_SP.collect_licensing_debts(
                                parser_input_param
                            )
                        )
                    )
                case _:
                    raise Exception("opção inválida")

        except Exception as exc:
            print(exc)
