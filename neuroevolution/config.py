from enum import Enum
from typing import List, Type, Union, Tuple
from neuroevolution.controllers import NetworkController
from neuroevolution.controllers import ProblemController
import inspect


class ParentChoosingMethod(Enum):
    RANDOM = 1
    SHIFTED_ROULETTE = 2


class Config:
    def __init__(self, input_size: int, output_size: int,
                 network_ctrler_cls: Type[NetworkController], problem_ctrler_cls: Type[ProblemController]):
        self.input_size: int = input_size
        self.output_size: int = output_size
        self.network_ctrler_cls: Type[NetworkController] = network_ctrler_cls
        self.problem_ctrler_cls: Type[ProblemController] = problem_ctrler_cls

        self.save_progress = False
        self.save_logs = False
        self.log_file_name = None
        self.save_csv = False
        self.csv_file_name = None

        self.fitness_target: Union[None, float] = None
        self.max_iterations: int = 1000
        self.stagnation_limit: Union[None, int] = 30
        self.max_existing_species: int = 3

        self.allow_recurrent: bool = False
        self.has_bias_neuron: bool = False
        self.output_function: str = "RELU"
        self.hidden_functions_set: List[str] = ["RELU"]

        self.offspring_quantity: int = 100
        self.breeding_percentage: float = 0.5  # eg. 50% of best individuals will mate...
        self.survival_percentage: float = 0.25  # ... but after that 25% OF THEM will go to next population
        self.parent_choosing_method: ParentChoosingMethod = ParentChoosingMethod.RANDOM
        self.new_species_clones_amount: int = 99

        # initializing
        self.init_connection_prob: float = 1.0
        self.weight_interval: Tuple[float, float] = (-2.0, 2.0)

        # crossover
        self.average_crossover_chance: float = 0.05
        self.weight_shift_standard_deviation: float = 0.05

        # mutations
        self.max_mutations_once: int = 1

        self.do_new_link_mutation: bool = True
        self.new_link_prob: float = 0.05

        self.do_divide_link_mutation: bool = True
        self.divide_link_prob: float = 0.001
        self.disabling_prob: float = 0.5

        self.do_alter_disabled_mutation: bool = True
        self.alter_disabled_prob: float = 0.01

        self.do_enable_link_mutation: bool = False
        self.enable_link_prob: float = 0.01

        self.do_weight_shift_mutation: bool = False
        self.weight_shift_prob: float = 0.1
        self.weight_shift_interval: Tuple[float, float] = (-1.5, 1.5)

        self.do_randomize_weight_mutation: bool = False
        self.randomize_weight_prob: float = 0.1

        self.do_randomize_all_weights_mutation: bool = False
        self.randomize_all_weights_prob: float = 0.05
        self.single_randomization_prob: float = 0.75

        # testing
        self.test_processes: int = 2

    class WrongType(Exception):
        def __init__(self, message):
            super().__init__(message)

    @staticmethod
    def validate(dictionary, key, types):
        if not isinstance(dictionary[key], types):
            raise Config.WrongType(key)

    @classmethod
    def load_from_dict(cls, dictionary):
        # MANDATORY PARAMETERS
        Config.validate(dictionary, "input size", int)
        Config.validate(dictionary, "output size", int)
        if not inspect.isclass(dictionary["network controller class"]):
            raise Config.WrongType("network controller class")
        if not inspect.isclass(dictionary["problem controller class"]):
            raise Config.WrongType("problem controller class")

        config = cls(dictionary["input size"], dictionary["output size"], dictionary["network controller class"], dictionary["problem controller class"])

        Config.validate(dictionary, "fitness target", (float, type(None)))
        config.fitness_target = dictionary["fitness target"]

        Config.validate(dictionary, "max iterations", int)
        config.max_iterations = dictionary["max iterations"]

        Config.validate(dictionary, "output function", str)
        config.output_function = dictionary["output function"]

        Config.validate(dictionary, "hidden functions set", str)
        config.hidden_functions_set = dictionary["hidden functions set"].split()

        Config.validate(dictionary, "min link weight", float)
        Config.validate(dictionary, "max link weight", float)
        config.weight_interval = (dictionary["min link weight"], dictionary["max link weight"])

        Config.validate(dictionary, "weight shift standard deviation", float)
        config.weight_shift_standard_deviation = dictionary["weight shift standard deviation"]

        Config.validate(dictionary, "test processes", int)
        config.test_processes = dictionary["test processes"]

        # PRIMARY PARAMETERS
        if dictionary.get("offspring quantity") is not None:
            Config.validate(dictionary, "offspring quantity", int)
            config.offspring_quantity = dictionary.get("offspring quantity")
        config.new_species_clones_amount = config.offspring_quantity-1

        if dictionary.get("breeding percentage") is not None:
            Config.validate(dictionary, "breeding percentage", float)
            config.breeding_percentage = dictionary.get("breeding percentage")

        if dictionary.get("survival percentage") is not None:
            Config.validate(dictionary, "survival percentage", float)
            config.survival_percentage = dictionary.get("survival percentage")

        if dictionary.get("stagnation limit") is not None:
            Config.validate(dictionary, "stagnation limit", int)
            config.stagnation_limit = dictionary.get("stagnation limit")

        if dictionary.get("max existing species") is not None:
            Config.validate(dictionary, "max existing species", int)
            config.max_existing_species = dictionary.get("max existing species")

        if dictionary.get("parent choosing method") is not None:
            Config.validate(dictionary, "parent choosing method", str)
            if dictionary.get("parent choosing method") == "roulette":
                config.parent_choosing_method = ParentChoosingMethod.SHIFTED_ROULETTE
            else:
                config.parent_choosing_method = ParentChoosingMethod.RANDOM

        # MUTATION PARAMETERS
        if dictionary.get("max mutations once") is not None:
            Config.validate(dictionary, "max mutations once", int)
            config.max_mutations_once = dictionary.get("max mutations once")

        if dictionary.get("do new link mutation") is not None:
            Config.validate(dictionary, "do new link mutation", bool)
            config.do_new_link_mutation = dictionary.get("do new link mutation")

        if dictionary.get("new link mutation prob") is not None:
            Config.validate(dictionary, "new link mutation prob", float)
            config.new_link_prob = dictionary.get("new link mutation prob")

        if dictionary.get("do divide link mutation") is not None:
            Config.validate(dictionary, "do divide link mutation", bool)
            config.do_divide_link_mutation = dictionary.get("do divide link mutation")

        if dictionary.get("divide link prob") is not None:
            Config.validate(dictionary, "divide link prob", float)
            config.divide_link_prob = dictionary.get("divide link prob")

        if dictionary.get("disabling prob") is not None:
            Config.validate(dictionary, "disabling prob", float)
            config.disabling_prob = dictionary.get("disabling prob")

        if dictionary.get("do alter disabled mutation") is not None:
            Config.validate(dictionary, "do alter disabled mutation", bool)
            config.do_alter_disabled_mutation = dictionary.get("do alter disabled mutation")

        if dictionary.get("alter disabled prob") is not None:
            Config.validate(dictionary, "alter disabled prob", float)
            config.alter_disabled_prob = dictionary.get("alter disabled prob")

        if dictionary.get("do enable link mutation") is not None:
            Config.validate(dictionary, "do enable link mutation", bool)
            config.do_enable_link_mutation = dictionary.get("do enable link mutation")

        if dictionary.get("enable link prob") is not None:
            Config.validate(dictionary, "enable link prob", float)
            config.enable_link_prob = dictionary.get("enable link prob")

        if dictionary.get("do weight shift mutation") is not None:
            Config.validate(dictionary, "do weight shift mutation", bool)
            config.do_weight_shift_mutation = dictionary.get("do weight shift mutation")

        if dictionary.get("weight shift prob") is not None:
            Config.validate(dictionary, "weight shift prob", float)
            config.weight_shift_prob = dictionary.get("weight shift prob")

        if dictionary.get("min weight shift multiplier") is not None and dictionary.get("max weight shift multiplier") is not None:
            Config.validate(dictionary, "min weight shift multiplier", float)
            Config.validate(dictionary, "max weight shift multiplier", float)
            config.weight_shift_interval = (dictionary.get("min weight shift multiplier"), dictionary.get("max weight shift multiplier"))

        if dictionary.get("do randomize weight mutation") is not None:
            Config.validate(dictionary, "do randomize weight mutation", bool)
            config.do_randomize_weight_mutation = dictionary.get("do randomize weight mutation")

        if dictionary.get("randomize weight prob") is not None:
            Config.validate(dictionary, "randomize weight prob", float)
            config.randomize_weight_prob = dictionary.get("randomize weight prob")

        if dictionary.get("do randomize all weights mutation") is not None:
            Config.validate(dictionary, "do randomize all weights mutation", bool)
            config.do_randomize_all_weights_mutation = dictionary.get("do randomize all weights mutation")

        if dictionary.get("randomize all weights prob") is not None:
            Config.validate(dictionary, "randomize all weights prob", float)
            config.randomize_all_weights_prob = dictionary.get("randomize all weights prob")

        if dictionary.get("single randomization prob") is not None:
            Config.validate(dictionary, "single randomization prob", float)
            config.single_randomization_prob = dictionary.get("single randomization prob")

        # ADVANCED PARAMETERS
        if dictionary.get("init connection prob") is not None:
            Config.validate(dictionary, "init connection prob", float)
            config.init_connection_prob = dictionary.get("init connection prob")

        if dictionary.get("average crossover chance") is not None:
            Config.validate(dictionary, "average crossover chance", float)
            config.average_crossover_chance = dictionary.get("average crossover chance")

        if dictionary.get("allow recurrent") is not None:
            Config.validate(dictionary, "allow recurrent", bool)
            config.allow_recurrent = dictionary.get("allow recurrent")

        if dictionary.get("has bias neuron") is not None:
            Config.validate(dictionary, "has bias neuron", bool)
            config.has_bias_neuron = dictionary.get("has bias neuron")

        # SAVING OPTIONS
        if dictionary.get("save progress") is not None:
            Config.validate(dictionary, "save progress", bool)
            config.save_progress = dictionary.get("save progress")

        if dictionary.get("save logs") is not None:
            Config.validate(dictionary, "save logs", bool)
            config.save_logs = dictionary.get("save logs")

        if dictionary.get("log file name") is not None:
            Config.validate(dictionary, "log file name", str)
            config.log_file_name = dictionary.get("log file name")

        if dictionary.get("save csv") is not None:
            Config.validate(dictionary, "save csv", bool)
            config.save_csv = dictionary.get("save csv")

        if dictionary.get("csv file name") is not None:
            Config.validate(dictionary, "csv file name", str)
            config.csv_file_name = dictionary.get("csv file name")

        return config
