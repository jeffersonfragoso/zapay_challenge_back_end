import json
import pathlib
from unittest.mock import Mock

import pytest
from jsonschema import validate

from core.debts.application.SP.services import SPService


@pytest.fixture
def sp_service():
    params = {"license_plate": "ABC1234", "renavam": "11111111111"}

    sp_service = SPService(params=params)
    yield sp_service


def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(f"{pathlib.Path(__file__).parent.absolute()}/json_schemas")
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(payload, schema)


@pytest.mark.parametrize(
    "method, schema_name",
    [
        ("ConsultaMultas", "Multas.json"),
        ("ConsultaIPVA", "IPVAs.json"),
        ("ConsultaDPVAT", "DPVATs.json"),
        ("ConsultaLicenciamento", "Licenciamento.json"),
    ],
)
def test_get_json_response(sp_service, method, schema_name):
    """
    GIVEN consultar débitos na api de SP
    WHEN get_json_response for executado
    THEN deve retornar uma response no formato json que corresponde ao schema.
    """
    response = sp_service.get_json_response(method)
    validate_payload(response, schema_name)


@pytest.mark.parametrize(
    "mercosul_plate, gray_plate",
    [
        ("ABC1C34", "ABC1234"),
        ("ACI6J67", "ACI6967"),
        ("ABC1C34", "ABC1234"),
        ("MAA0B92", "MAA0192"),
        ("BCG7G17", "BCG7617"),
        ("FAL7D00", "FAL7300"),
        ("HAH2H74", "HAH2774"),
        ("POD5A60", "POD5060"),
    ],
)
def test_convert_to_gray_plate(sp_service, mercosul_plate, gray_plate):
    """
    GIVEN consultar débitos na api de SP
    WHEN uma placa no padrão 'Mercosul' for informada
    AND convert_to_gray_plate for executado
    THEN deve retornar uma placa no padrão 'Gray'.
    """
    assert gray_plate == sp_service._convert_to_gray_plate(mercosul_plate)


@pytest.mark.parametrize(
    "debt_option, call_option",
    [
        ("ticket", "ConsultaMultas"),
        ("ipva", "ConsultaIPVA"),
        ("dpvat", "ConsultaDPVAT"),
        ("licensing", "ConsultaLicenciamento"),
        ("", ""),
    ],
)
def test_debt_search_options(sp_service, debt_option, call_option):
    """
    GIVEN consultar débitos na api de SP
    WHEN uma debt_option for informada
    THEN get_json_response deve ser executado para a opção correspodente.
    WHEN debt_option não for informada
    THEN get_json_response deve ser executado para as 4 opções possíveis.
    """
    sp_service.params.update({"debt_option": debt_option})
    sp_service.get_json_response = Mock()
    sp_service.debt_search()

    if debt_option:
        sp_service.get_json_response.assert_called_with(call_option)
    else:
        assert sp_service.get_json_response.call_count == 4
