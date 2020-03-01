from os import path
import csv


class LogUtil:
    @staticmethod
    def proceed(nev_instance, save_to_file: bool):
        info_string = LogUtil.get_info_string(nev_instance)
        print(info_string)
        if save_to_file:
            LogUtil.write_to_file(info_string, nev_instance)

    @staticmethod
    def get_info_string(nev_instance):
        best_genome = nev_instance.best_genome
        info_string = "==========[Gen: " + str(
            nev_instance.current_iteration) + " ]Best individual:==========\n"
        info_string += str(best_genome)

        population_string = "\n\nPopulation count: " + str(
            nev_instance.current_population.get_population_real_size())
        population_string += " (Survivors: " + str(len(nev_instance.current_population.survivors))
        population_string += " New individuals: " + str(len(nev_instance.current_population.new_genomes)) + ")"

        info_string += population_string
        info_string += "\nSpecies count: " + str(len(nev_instance.species)) + "\n\n"

        return info_string

    @staticmethod
    def write_to_file(string, nev_instance):
        file_name = nev_instance.config.log_file_name
        if file_name is None:
            file_name = "log" + str(id(nev_instance)) + ".txt"

        open_attribute = "a" if path.exists(file_name) else "w"
        with open(file_name, open_attribute) as log_file:
            log_file.write(string)


class CsvUtil:
    @staticmethod
    def proceed(nev_instance):
        file_name = nev_instance.config.csv_file_name
        if file_name is None:
            file_name = "fitnesses" + str(id(nev_instance)) + ".csv"

        open_attribute = "a" if path.exists(file_name) else "w"
        with open(file_name, open_attribute) as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(nev_instance.current_population.get_fitness_list())
