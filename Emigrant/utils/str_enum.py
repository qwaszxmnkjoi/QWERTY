"""
String Enumeration Base
"""

__all__ = ['StrEnumBase', 'StrEnumDataBase']

# Standard library imports.
import enum
import typing

# Related third party imports.
from django.utils.safestring import mark_safe

# Local application/library specific imports.


class StrEnumBase(str, enum.Enum):
    @classmethod
    def as_choices(cls) -> typing.Tuple[typing.Tuple['StrEnumBase', str], ...]:
        raise NotImplementedError()

    @classmethod
    def as_model_choices(cls) -> typing.Tuple[typing.Tuple[str, str], ...]:
        return tuple([(val[0].as_str, val[1]) for val in cls.as_choices()])

    @classmethod
    def as_dict(cls) -> typing.Dict['StrEnumBase', str]:
        return dict(cls.as_choices())

    @classmethod
    def as_dict_str_key(cls) -> typing.Dict[str, str]:
        return dict(cls.as_model_choices())

    @classmethod
    def as_set(cls) -> typing.Set['StrEnumBase']:
        return set(cls.as_dict().keys())

    @classmethod
    def as_set_str(cls) -> typing.Set[str]:
        return {val.as_str for val in cls.as_set()}

    @classmethod
    def as_list(cls) -> typing.List['StrEnumBase']:
        return list(cls.as_dict().keys())

    @classmethod
    def as_list_str(cls) -> typing.List[str]:
        return [val.as_str for val in cls.as_set()]

    @classmethod
    def as_tuple(cls) -> typing.Tuple['StrEnumBase', ...]:
        return tuple(cls.as_list())

    @classmethod
    def as_tuple_str(cls) -> typing.Tuple[str, ...]:
        return tuple(cls.as_list_str())

    @property
    def as_str(self) -> str:
        return str(self.value)

    @property
    def as_readable(self) -> str:
        return str(self.as_dict()[self.value])

    @classmethod
    def cast_default_value(cls) -> typing.Optional['StrEnumBase']:
        return None

    @classmethod
    def help_text(cls) -> str:
        template = '<li><strong>{name}</strong> - {readable}</li>'
        items = [
            template.format(name=name, readable=readable)
            for name, readable in cls.as_model_choices()
        ]
        result = f'<ul>{"".join(items)}</ul>'
        return result

    @classmethod
    def help_text_safe(cls):
        return cls.mark_safe(cls.help_text())

    @classmethod
    def mark_safe(cls, text: str) -> str:
        return mark_safe(text)

    @classmethod
    def cast(cls, value: typing.Union[str, 'StrEnumBase'],
             default: typing.Optional['StrEnumBase'] = None, skip_none: bool = False,
             raise_exceptions: bool = True) -> typing.Optional['StrEnumBase']:
        """
        Cast provided `level` to `StrEnumBase` based on next rules:

        * if level is of type `StrEnumBase` then returns level
        * if level is of type `str` and can be casted to `StrEnumBase` then returns casted level
        * if level is of type `str` and can not be casted to `StrEnumBase` and `raise_exceptions=True` then raise Exception
        * otherwise returns `default`: if `default` is None then returns `cls.cast_default_value()`

        :param value:
        :param default:
        :param skip_none:
        :param raise_exceptions:
        :return: StrEnumBase
        """
        default = default or cls.cast_default_value()
        result = value or default

        if value is None:
            if not skip_none:
                raise ValueError(f'Value can not be `None`')
        elif not isinstance(value, cls):
            try:
                result = cls(value)
            except Exception as e:
                if raise_exceptions:
                    raise e
                result = default

        return result

    def __str__(self):
        return self.as_str


class StrEnumDataBase:
    value_cls: typing.Type[StrEnumBase] = StrEnumBase

    def __init__(self, value: typing.Union[str, 'StrEnumBase', None]):
        if isinstance(value, str):
            self._value = self.value_cls(value)
        elif isinstance(value, self.value_cls):
            self._value = value
        elif value is None:
            self._value = None
        else:
            raise Exception(f'`value` must be `None` or of type `str`, `{self.value_cls.__name__}` but got `{type(value).__name__}`')

    @property
    def as_typed(self) -> typing.Optional['StrEnumBase']:
        return self._value

    @property
    def as_str(self) -> typing.Optional[str]:
        return self.as_typed.as_str if self.as_typed else None

    @property
    def as_readable(self) -> typing.Optional[str]:
        return str(self.value_cls.as_dict()[self.as_typed]) if self.as_typed else None

    def compare(self, other: 'StrEnumBase') -> typing.Optional[bool]:
        return self.as_typed == other if self.as_typed else None

    def __getattr__(self, item: str):
        if item.startswith('is_'):
            item = item.replace('is_', '')

            is_nre = True
            if item.endswith('_nre'):
                item = item.replace('_nre', '')
                is_nre = False

            return self.compare(self.value_cls.cast(item, raise_exceptions=is_nre))
        else:
            raise AttributeError
