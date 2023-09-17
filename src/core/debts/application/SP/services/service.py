from dataclasses import dataclass, field
from typing import Dict

from core.debts.application.SP.services.api import API


@dataclass(kw_only=True, slots=True)
class SPService:
    """
    Conecta com o webservice do Detran-SP.
    """

    params: Dict = field(default_factory=lambda: dict)
    tickets: Dict = field(default_factory=lambda: dict)
    ipvas: Dict = field(default_factory=lambda: dict)
    dpvats: Dict = field(default_factory=lambda: dict)
    licensing: Dict = field(default_factory=lambda: dict)

    def execute(self, **kwargs) -> Dict:
        self.params = kwargs
        return self.debt_search()

    def _convert_to_gray_plate(self, license_plate):
        mercosul_map_converter = {
            "A": "0",
            "B": "1",
            "C": "2",
            "D": "3",
            "E": "4",
            "F": "5",
            "G": "6",
            "H": "7",
            "I": "8",
            "J": "9",
        }

        license_plate_split = list(license_plate)
        license_plate_split[4] = mercosul_map_converter[license_plate_split[4].upper()]
        license_plate = "".join(license_plate_split)

        return license_plate

    def get_json_response(self, method):
        """
        Pega a resposta da requisição em json.
        """
        license_plate = self.params["license_plate"]

        if license_plate[4].isalpha():
            license_plate = self._convert_to_gray_plate(license_plate)

        return API(
            license_plate=license_plate,
            renavam=self.params["renavam"],
            debt_option=method,
        ).fetch()

    def debt_search(self):
        """
        Pega os débitos de acordo com a opção passada.
        """
        debt_option = self.params.get("debt_option", "")

        match debt_option:
            case "":
                self.tickets = self.get_json_response("ConsultaMultas").get(
                    "Multas", {}
                )
                self.ipvas = self.get_json_response("ConsultaIPVA").get("IPVAs", {})
                self.dpvats = self.get_json_response("ConsultaDPVAT").get("DPVATs", {})
                self.licensing = self.get_json_response("ConsultaLicenciamento")
            case "ticket":
                self.tickets = self.get_json_response("ConsultaMultas").get(
                    "Multas", {}
                )
            case "ipva":
                self.ipvas = self.get_json_response("ConsultaIPVA").get("IPVAs", {})
            case "dpvat":
                self.dpvats = self.get_json_response("ConsultaDPVAT").get("DPVATs", {})
            case "licensing":
                self.licensing = self.get_json_response("ConsultaLicenciamento")
            case _:
                raise Exception("opção inválida")

        debts = {
            "Multas": self.tickets,
            "IPVAs": self.ipvas,
            "DPVATs": self.dpvats,
            "Licenciamento": self.licensing,
        }

        for debt in debts:
            if debts[debt] == {}:
                debts[debt] = None

        return debts
