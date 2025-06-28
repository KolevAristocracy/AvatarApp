from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class LettersDigitsSpacesUnderscoreValidator:
    def __init__(self, message: str=None) -> None:
        self.message = message

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value or "*Allowed names contain letters, digits, spaces, and underscores."

    def __call__(self, value: str) -> None:
        for char in value:
            if not (char.isalnum() or char in [' ', '_']):
                raise ValidationError(self.message)