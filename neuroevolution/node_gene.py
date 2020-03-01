from enum import Enum
import random
from typing import List


class NodeType(Enum):
    INPUT = 1
    OUTPUT = 2
    HIDDEN = 3
    BIAS = 4


class NodeGene:
    def __init__(self, identifier: int, node_type: NodeType, act_function: str):
        self.identifier: int = identifier  # unique number of this gene
        self.node_type: NodeType = node_type
        self.act_function: str = act_function

    @classmethod
    def get_input(cls, identifier: int):
        return cls(identifier, NodeType.INPUT, "IDENTITY")

    @classmethod
    def get_output(cls, identifier: int, act_func: str):
        return cls(identifier, NodeType.OUTPUT, act_func)

    @classmethod
    def get_random_hidden(cls, identifier: int, func_list: List[str]):
        return cls(identifier, NodeType.HIDDEN, random.choice(func_list))

    @classmethod
    def get_bias(cls, identifier: int):
        return cls(identifier, NodeType.BIAS, "IDENTITY")
