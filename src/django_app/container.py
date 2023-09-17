from dependency_injector import containers, providers

from core.debts.application.SP.services import SPParser, SPService
from core.debts.application.SP.use_case import SearchcDebtsUseCase
from core.debts.application.use_cases import (
    CreateDPVATUseCase,
    CreateIPVAUseCase,
    CreateLicenciamentoUseCase,
    CreateMultaUseCase,
)


class Container(containers.DeclarativeContainer):
    use_case_create_multa = providers.Singleton(CreateMultaUseCase)
    use_case_create_IPVA = providers.Singleton(CreateIPVAUseCase)
    use_case_create_DPVAT = providers.Singleton(CreateDPVATUseCase)
    use_case_create_licenciamento = providers.Singleton(CreateLicenciamentoUseCase)

    application_service_SPParser = providers.Singleton(
        SPParser,
        use_case_create_IPVA=use_case_create_IPVA,
        use_case_create_multa=use_case_create_multa,
        use_case_create_DPVAT=use_case_create_DPVAT,
        use_case_create_licenciamento=use_case_create_licenciamento,
    )

    application_service_SPService = providers.Singleton(SPService)

    use_case_search_debts_sp = providers.Singleton(
        SearchcDebtsUseCase,
        service_parser_SP=application_service_SPParser,
        service_detran_SP=application_service_SPService,
    )


container = Container()
