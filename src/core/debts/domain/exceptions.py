from typing import Dict, List


class EntityValidationException(Exception):
    error: Dict[str, List[str]]

    def __init__(self, error: Dict[str, List[str]]) -> None:
        self.error = error
        super().__init__("Entity Validation Error")
