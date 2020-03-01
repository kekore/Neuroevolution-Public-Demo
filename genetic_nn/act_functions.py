import math


class FuncAbstract:
    """Abstract class for activation functions"""
    @staticmethod
    def func(x: float):
        pass


class Sigmoid(FuncAbstract):
    @staticmethod
    def func(x: float) -> float:
        return 1/(1+math.exp(-x))


class Sigmoid5(FuncAbstract):
    @staticmethod
    def func(x: float) -> float:
        return 1 / (1 + math.exp(-5 * x))


class Identity(FuncAbstract):
    @staticmethod
    def func(x: float) -> float:
        return x


class TanH(FuncAbstract):
    @staticmethod
    def func(x: float) -> float:
        a = math.exp(x) - math.exp(-x)
        b = math.exp(x) + math.exp(-x)
        return a/b


class BinaryStep(FuncAbstract):
    @staticmethod
    def func(x: float) -> float:
        if x < 0:
            return 0
        return 1


class Relu(FuncAbstract):
    @staticmethod
    def func(x: float) -> float:
        if x < 0:
            return 0
        return x
