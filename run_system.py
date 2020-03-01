import importlib.util
import sys
import inspect
import json
from neuroevolution.config import Config
from neuroevolution.neuroevolution import Neuroevolution
from neuroevolution.genome import Genome


class ClassNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class ClassFileNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


def load_class(filepath, module_name, class_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    for name, obj in inspect.getmembers(sys.modules[module_name]):
        if name == class_name:
            return obj
    raise ClassNotFound(class_name + " not found in file \"" + filepath + "\"")


def load_config_to_dict(file_path):
    with open(file_path, 'r') as f:
        dictionary = json.load(f)

    net_string = "network controller class"
    prob_string = "problem controller class"
    try:
        dictionary[net_string] = load_class(dictionary[net_string + " filepath"], "user_net_module", dictionary[net_string + " name"])
    except FileNotFoundError:
        raise ClassFileNotFound("Filepath: \"" + dictionary[net_string + " filepath"] + "\" given as \"" + net_string + " filepath\" not found!")
    try:
        dictionary[prob_string] = load_class(dictionary[prob_string + " filepath"], "user_prob_module", dictionary[prob_string + " name"])
    except FileNotFoundError:
        raise ClassFileNotFound("Filepath: \"" + dictionary[prob_string + " filepath"] + "\" given as \"" + prob_string + " filepath\" not found!")
    return dictionary


if __name__ == '__main__':
    try:
        config_dictionary = load_config_to_dict(sys.argv[1])
    except json.JSONDecodeError:
        print("Given config file is not a valid JSON file!")
        exit()
    except FileNotFoundError:
        print("Config file not found!")
        exit()
    except KeyError as ke:
        print("Mandatory parameter " + str(ke) + " not set!")
        exit()
    except ClassNotFound as cnf:
        print(str(cnf))
        exit()
    except ClassFileNotFound as cfnf:
        print(str(cfnf))
        exit()

    # check if resume
    if len(sys.argv) == 4 and sys.argv[2] == "resume":
        nev = Neuroevolution.load_alg(sys.argv[3])
        nev.proceed()
    # else - check if demo
    elif len(sys.argv) == 4 and sys.argv[2] == "demo":
        genome = Genome.load(sys.argv[3])
        print(genome.nodes_genome)
        print(genome.links_genome)
        network_controller = config_dictionary["network controller class"](genome)
        problem_controller = config_dictionary["problem controller class"](network_controller, -1)
        problem_controller.run_test()
    # else - new algorithm instance
    elif len(sys.argv) == 2:
        try:
            config = Config.load_from_dict(config_dictionary)
        except KeyError as ke:
            print("Mandatory parameter " + str(ke) + " not set!")
            exit()
        except Config.WrongType as wt:
            print("Wrong type of parameter " + str(wt) + " in config file!")
            exit()
        nev = Neuroevolution(config)
        nev.proceed()
