"""
Date: 2023-03-28
Class: TransistorMeta
Description: Singleton pattern, it's responsible only for making sure, only one Transistor object is created.

Class: Bjt
Description: Bjt is a dataclass which contains only bjt transistor parameters.

Class: Transistor
Description: It provides and represents all transistors. Initialised in a Circuit class.
"""
from dataclasses import dataclass, field
from parts import TransistorsBlueprint


class TransistorMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            raise Exception("Only one Transistor object is allowed!")


@dataclass(order=True, frozen=True)
class Bjt(object):
    # order=True enables sorting objects by any value defined in __post_init__ assigned to sort_index
    # frozen=True, read-only. It allows to make sure data is not changed anywhere in code
    """
    model: str - Model of a transistor
    hfe: int - hfe/beta
    type: str - NPN or PNP
    vbe: float - Voltage drop between emitter and base, default 0.7
    re??: float - internal_emitter_voltage_drop, const value = 0.025 mV
    """
    model: str
    hfe: int
    type: str
    vbe: float = 0.7
    internal_emitter_voltage_drop: float = 0.025
    # use it just as field for sorting, so you don't need to initialise it in object creation
    sort_index: int = field(init=False, repr=False)

    def __post_init__(self):
        # self.sort_index = self.hfe      # can't assign it directly with frozen=True (it's read only)
        object.__setattr__(self, 'sort_index', self.hfe)

    def __str__(self) -> str:
        return f"Model: {self.model}, Type {self.type}, Hfe: {self.hfe}, Vbe: {self.vbe}, Memory ID: {id(self)}"


class Transistor(metaclass=TransistorMeta):
    def __init__(self, transistors_blueprint: type(TransistorsBlueprint)):
        """
        :param transistors_blueprint: TransistorsBlueprint Dataclass
        """
        self.__transistors: dict[str, Bjt] = {}
        self.__transistors_blueprint: dict[str, dict[str, str | int]] = transistors_blueprint().transistors
        self.initialise_bjt_transistors()

    def __call__(self, model: str) -> Bjt:
        """Can use object as function"""
        return self.__transistors[model]

    @property
    def transistors(self) -> dict[str, Bjt]:
        return self.__transistors

    def initialise_bjt_transistors(self):
        for q in self.__transistors_blueprint:
            new_transistor: Bjt = Bjt(**self.__transistors_blueprint[q])

            if new_transistor.model not in self.__transistors.keys():
                self.__transistors[new_transistor.model] = new_transistor

    def sort_transistors_by_name(self):
        # TODO: use some sorting algorithm (quick sort??)
        for model, transistor in self.__transistors:
            pass

    def sort_transistors_by_hfe(self):
        pass
