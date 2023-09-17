from django.urls import path

from django_app.container import container

from .api import DebtResource

urlpatterns = [
    path(
        "debts/",
        DebtResource.as_view(
            use_case_search_debts_SP=container.use_case_search_debts_sp,
        ),
    )
]
