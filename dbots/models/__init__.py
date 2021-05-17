from datetime import datetime
from typing import get_args


def parse_dict(value, t: type):
    if isinstance(value, Model):
        return value.__dict__()
    elif t == datetime:
        return value.isoformat()
    else:
        return value


def parse_raw_value(value, t: type):
    if t == bool and type(value) == str:
        return value.lower() in {"true", "yes"}
    if issubclass(t, Model) and type(value) == dict:
        return t.from_dict(value)
    if t == datetime:
        return datetime.fromisoformat(value)
    if "list[" in str(t) and type(value) == list:
        list_type = get_args(t)[0]
        return [parse_raw_value(x, list_type) for x in value]
    return t(value)


class Model:
    @classmethod
    def from_dict(cls, d: dict):
        new_dict = {}
        for k, v in cls.__annotations__.items():
            if k in d:
                new_dict[k] = parse_raw_value(d[k], v)
            else:
                new_dict[k] = None
        return cls(**new_dict)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.__annotations__:
                setattr(self, k, v)

    def __dict__(self) -> dict:
        d = {}
        for k, v in self.__annotations__.items():
            d[k] = parse_dict(getattr(self, k), self.__annotations__[k])
        return d

    def __repr__(self):
        return str(self.__dict__())


class ActionDoneModel(Model):
    code: int
    message: str
