from dataclasses import asdict, dataclass
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.debts.application.dto import SearchDebtsInput
from core.debts.application.SP.use_case import SearchcDebtsUseCase


@dataclass(slots=True)
class DebtResource(APIView):
    use_case_search_debts_SP: Callable[[], SearchcDebtsUseCase]

    def get(self, request: Request):
        input_param = SearchDebtsInput(**request.query_params.dict())

        output = next(self.use_case_search_debts_SP().execute(input_param))
        return Response(asdict(output))
