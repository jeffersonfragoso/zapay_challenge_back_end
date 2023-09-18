import pytest

from core.debts.application.dto import (
    DPVATOutput,
    IPVAOutput,
    LicenciamentoOutput,
    MultaOutput,
    SPParserInput,
)
from core.debts.application.SP.services import SPParser
from core.debts.application.use_cases import (
    CreateDPVATUseCase,
    CreateIPVAUseCase,
    CreateLicenciamentoUseCase,
    CreateMultaUseCase,
)
from core.debts.tests.application.SP.services.responses_SP import (
    ConsultaDPVAT,
    ConsultaIPVA,
    ConsultaMultas,
    Licenciamento,
)


@pytest.fixture()
def sp_service_output():
    sp_service_output = {
        "Multas": None,
        "IPVAs": None,
        "DPVATs": None,
        "Licenciamento": None,
    }

    yield sp_service_output


@pytest.fixture()
def sp_parser():
    sp_parser = SPParser(
        use_case_create_multa=CreateMultaUseCase(),
        use_case_create_DPVAT=CreateDPVATUseCase(),
        use_case_create_IPVA=CreateIPVAUseCase(),
        use_case_create_licenciamento=CreateLicenciamentoUseCase(),
    )

    yield sp_parser


def test_collect_ipva_debts(sp_service_output, sp_parser):
    """
    GIVEN parsear responses da api de SP
    WHEN collect_ipva_debts for executado
    THEN deve retornar a lista com itens no padrão 'IPVAOutput'
    """

    sp_service_output.update({"IPVAs": ConsultaIPVA.json.get("IPVAs")})

    expected_result = [
        IPVAOutput(
            **{
                "amount": 1365.69,
                "description": "IPVA 2021",
                "installment": "unique",
                "title": "IPVA - Cota Única",
                "type": "ipva",
                "year": 2021,
            }
        ),
        IPVAOutput(
            **{
                "amount": 1012.5,
                "description": "IPVA 2020",
                "installment": 2,
                "title": "IPVA - Cota 2",
                "type": "ipva",
                "year": 2020,
            }
        ),
    ]

    parsed_ipvas = list(
        sp_parser.collect_ipva_debts(SPParserInput(data=sp_service_output))
    )

    assert parsed_ipvas == expected_result


def test_collect_ticket_debts(sp_service_output, sp_parser):
    """
    GIVEN parsear responses da api de SP
    WHEN collect_ticket_debts for executado
    THEN deve retornar a lista com itens no padrão 'MultaOutput'
    """

    sp_service_output.update({"Multas": ConsultaMultas.json.get("Multas")})

    expected_result = [
        MultaOutput(
            **{
                "amount": 201.18,
                "auto_infraction": "5E5E5E5E  ",
                "description": "Estacionar em Desacordo com a Sinalizacao.",
                "title": "Infração de Trânsito",
                "type": "ticket",
            }
        ),
        MultaOutput(
            **{
                "amount": 131.66,
                "auto_infraction": "6F6F6F6F  ",
                "description": "Trans. Veloc. Super. a Maxima Permitidaem Ate 20%.",
                "title": "Infração de Trânsito",
                "type": "ticket",
            }
        ),
    ]

    parsed_tickets = list(
        sp_parser.collect_ticket_debts(SPParserInput(data=sp_service_output))
    )

    assert parsed_tickets == expected_result


def test_collect_insurance_debts(sp_service_output, sp_parser):
    """
    GIVEN parsear responses da api de SP
    WHEN collect_insurance_debts for executado
    THEN deve retornar a lista com itens no padrão 'DPVATOutput'
    """
    sp_service_output.update({"DPVATs": ConsultaDPVAT.json.get("DPVATs")})
    expected_result = [
        DPVATOutput(
            **{
                "amount": 5.23,
                "description": "DPVAT 2020",
                "title": "Seguro Obrigatório",
                "type": "insurance",
                "year": 2020,
            }
        )
    ]

    parsed_dpvat = list(
        sp_parser.collect_insurance_debts(SPParserInput(data=sp_service_output))
    )

    assert parsed_dpvat == expected_result


def test_collect_licensing_debts(sp_service_output, sp_parser):
    """
    GIVEN parsear responses da api de SP
    WHEN collect_licensing_debts for executado
    THEN deve retornar o iten no padrão 'LicenciamentoOutput'
    """

    sp_service_output.update({"Licenciamento": Licenciamento.json})

    expected_result = [
        LicenciamentoOutput(
            **{
                "amount": 98.91,
                "description": "Licenciamento 2021",
                "title": "Licenciamento",
                "type": "licensing",
                "year": 2021,
            }
        )
    ]

    parsed_licenciamento = list(
        sp_parser.collect_licensing_debts(SPParserInput(data=sp_service_output))
    )

    assert parsed_licenciamento == expected_result


def test_collect_all_debts(sp_service_output, sp_parser):
    """
    GIVEN parsear responses da api de SP
    WHEN collect_all_debts for executado
    THEN deve executar todos os tipos de coleta de débitos
    """

    sp_service_output.update(
        {
            "Multas": ConsultaMultas.json.get("Multas"),
            "IPVAs": ConsultaIPVA.json.get("IPVAs"),
            "DPVATs": ConsultaDPVAT.json.get("DPVATs"),
            "Licenciamento": Licenciamento.json,
        }
    )

    parsed_all_debts = sp_parser.collect_all_debts(
        SPParserInput(data=sp_service_output)
    )
    assert isinstance(parsed_all_debts, list)
