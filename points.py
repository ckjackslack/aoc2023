from dataclasses import dataclass, field
from itertools import count
from typing import Optional


_priority = count(start=1)


@dataclass
class DescriptiveMixin:
    @property
    def row(self):
        return self.x

    @property
    def column(self):
        return self.y


@dataclass
class PriorityMixin:
    exclude_rules = {
        "_": [str.startswith],
        "Mixin": [str.endswith],
    }

    @classmethod
    def need_to_attach(cls):
        name = cls.__name__
        attach = True
        for part, fns in cls.exclude_rules.items():
            for fn in fns:
                if fn(name, part):
                    attach = False
                    break
            if not attach:
                break
        return attach

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.need_to_attach():
            cls._priority = next(_priority)

    def _determine_ret_cls(self, other):
        assert hasattr(self, "_priority")
        assert hasattr(other, "_priority")

        return (
            self.__class__
            if self._priority < other._priority
            else other.__class__
        )


@dataclass
class IntrospectiveAdditionMixin:
    def __add__(self, other):
        try:
            assert PriorityMixin in self.__class__.mro()
            _cls = self._determine_ret_cls(other)
            return _cls(self.x + other.x, self.y + other.y)
        except AssertionError:
            return self.__add__(other)


@dataclass
class ValidateMixin:
    _strict = False

    def __post_init__(self, *args, **kwargs):
        self._validate()

    def _is_integer(self, value):
        return type(value) == int

    def _is_non_negative(self, value):
        return value >= 0

    def _is_unsigned_int(self, value):
        return self._is_integer(value) and self._is_non_negative(value)

    def _validate(self):
        msg = r"Some args are not valid {}ints."
        values = self.as_tuple()
        if self._strict:
            if not all(self._is_unsigned_int(value) for value in values):
                raise ValueError(msg.format("unsigned "))
        else:
            if not all(self._is_integer(value) for value in values):
                raise ValueError(msg.format(""))


@dataclass
class DataMixin:
    data: Optional[object] = field(default=None)


@dataclass
class _Point(PriorityMixin):
    pass


@dataclass
class Point(ValidateMixin, _Point):
    x: int = field(default=0)
    y: int = field(default=0)

    @classmethod
    def from_tuple(cls, tup):
        return cls(*tup)

    @classmethod
    def from_coords(cls, x, y):
        return cls(x=x, y=y)

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        _cls = self.__class__
        assert isinstance(other, _cls)
        return _cls(self.x + other.x, self.y + other.y)


@dataclass
class _Cell(IntrospectiveAdditionMixin, Point, DescriptiveMixin):
    pass


@dataclass
class Cell(DataMixin, _Cell, PriorityMixin):
    pass


@dataclass
class Position(_Cell, PriorityMixin):
    pass


def main():
    from itertools import product
    from pprint import pp

    args = (0, 0)
    classes = (Point, Cell, Position)
    objects = [cls(*args) for cls in classes]

    # print(objects)

    # print([cls.from_tuple(args) for cls in classes])

    # print([cls.from_coords(*args) for cls in classes])

    # print([obj.as_tuple() for obj in objects])

    # props = ("_validate", "_determine_ret_cls", "row", "column", "data")
    # pp(
    #     [
    #         (
    #             cls.__name__,
    #             *[
    #                 f"{name}: {hasattr(cls, name)}"
    #                 for name
    #                 in props
    #             ]
    #         )
    #         for cls
    #         in classes
    #     ],
    #     width=50,
    # )

    # from inspect import signature
    # print(signature(Point))
    # print(signature(Cell))
    # print(signature(Position))

    # for c1, c2 in product(classes, classes):
    #     o1, o2 = c1(*args), c2(*args)
    #     result = o1 + o2
    #     print(f"{c1.__name__} + {c2.__name__} = {result}")

    # kwargs = dict(x=0, y=0, data="STRING")
    # print(Point(**kwargs))
    # print(Cell(**kwargs))
    # print(Position(**kwargs))


if __name__ == "__main__":
    main()
