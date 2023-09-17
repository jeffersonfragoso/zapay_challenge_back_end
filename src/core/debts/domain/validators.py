import abc
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List

from rest_framework import serializers
from rest_framework.fields import CharField, DictField, Field, FloatField, IntegerField


@dataclass(slots=True)
class ValidatorInterface(ABC):
    errors: Dict[str, List[str]] = None
    validated_data: Dict = None

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidatorAdapter(ValidatorInterface, ABC):
    def validate(self, data: serializers.Serializer):
        if data.is_valid():
            self.validated_data = dict(data.validated_data)
            return True

        self.errors = {
            field: [str(_error) for _error in _errors]
            for field, _errors in data.errors.items()
        }
        return False


class CharOrIntField(Field):
    def to_representation(self, value):
        try:
            if isinstance(value, int):
                return value
            elif isinstance(value, str):
                return value
        except TypeError:
            pass

        self.fail("invalid", input=value)

    def to_internal_value(self, data):
        try:
            if isinstance(data, int):
                return data
            elif isinstance(data, str):
                return data
        except TypeError:
            pass

        self.fail("invalid", input=data)


# Multa
class MultaDRFValidator(DRFValidatorAdapter):
    class MultaRules(serializers.Serializer):
        amount: FloatField(required=True)
        auto_infraction: CharField(required=True)
        description: CharField(required=True)
        title: CharField(required=True)
        type: CharField(required=True)

    def validate(self, data: Dict):
        rules = self.MultaRules(data=data if data is not None else {})
        return super().validate(rules)


class MultaValidatorFactory:
    @staticmethod
    def create():
        return MultaDRFValidator()


# IPVA
class IPVADRFValidator(DRFValidatorAdapter):
    class IPVARules(serializers.Serializer):
        amount: FloatField(required=True)
        description: CharField(required=False, allow_null=True, allow_blank=True)
        installment: CharOrIntField(required=False, allow_null=True)
        title: CharField(required=True)
        type: CharField(required=True)
        year: IntegerField(required=True)

    def validate(self, data: Dict):
        rules = self.IPVARules(data=data if data is not None else {})
        return super().validate(rules)


class IPVAValidatorFactory:
    @staticmethod
    def create():
        return IPVADRFValidator()


# DPVAT
class DPVATDRFValidator(DRFValidatorAdapter):
    class DPVATRules(serializers.Serializer):
        amount: FloatField(required=True)
        description: CharField(required=False, allow_null=True, allow_blank=True)
        title: CharField(required=True)
        type: CharField(required=True)
        year: IntegerField(required=True)

    def validate(self, data: Dict):
        rules = self.DPVATRules(data=data if data is not None else {})
        return super().validate(rules)


class DPVATValidatorFactory:
    @staticmethod
    def create():
        return DPVATDRFValidator()


# Licenciamento
class LicenciamentoValidator(DRFValidatorAdapter):
    class LicenciamentoRules(serializers.Serializer):
        amount: FloatField(required=True)
        description: CharField(required=False, allow_null=True, allow_blank=True)
        title: CharField(required=True)
        type: CharField(required=True)
        year: IntegerField(required=True)

    def validate(self, data: Dict):
        rules = self.LicenciamentoRules(data=data if data is not None else {})
        return super().validate(rules)


class LicenciamentoValidatorFactory:
    @staticmethod
    def create():
        return LicenciamentoValidator()


# SPParser
class SPParserValidator(DRFValidatorAdapter):
    class SPParsertoRules(serializers.Serializer):
        data: DictField(required=True)

    def validate(self, data: Dict):
        rules = self.SPParserRules(data=data if data is not None else {})
        return super().validate(rules)


class SPParserValidatorFactory:
    @staticmethod
    def create():
        return SPParserValidator()
