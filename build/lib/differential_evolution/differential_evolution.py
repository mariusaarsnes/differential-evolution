"""A Simple interface for Differential Evolution.

The Interface expects a Individual class with the following parameters and methods:

    parameters
    ------------------------------
    - genotype: a 1D list of values
    - fitness: a value scoring an individual
    - dimensions: the dimensions of the problem, i.e. the length of the genotype


    methods
    ------------------------------
    calculate_fitness(): a method to evaluate an individual
    generate_genotype(): a method to randomly instantiate the genotype of an individual





"""
from random import shuffle as _shuffle, randint as _randint, random as _random
from matplotlib import pyplot as _plt
from functools import reduce as _reduce

__all__ = ["DifferentialEvolution", "search", "plot_history"]


class DifferentialEvolution():
    """Differential Evolution base class.

    Used to instantiate instances of differential evolution.

    Assumes the presence of an Individual class which is used to represent the population
    and evaluate individuals.
    """

    def __init__(self, Individual, population_size=20, generations=5000, number_of_mutagens=3, F=1, CR=0.5
                 ):
        """Initialize an instance.

        """

        self.Individual = Individual
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.number_of_mutagens = number_of_mutagens
        self.CR = CR
        self.F = F

        self.history = []

    def _valid_instance(self):
        return self.Individual and self.population_size

    def _validate_instance(self):
        if not self._valid_instance():
            raise RuntimeError(
                "The instance is not valid - missing either an Individual or a population size")

    def _initialize_population(self):
        new_population = []
        for _ in range(self.population_size):
            new_population.append(self._initialize_individual())
        self.population = new_population

    def _initialize_individual(self):
        new_individual = self.Individual()
        new_individual.generate_genotype()
        new_individual.calculate_fitness()
        return new_individual

    def _get_best_individual(self):
        return _reduce(lambda individual_1, individual_2: individual_1 if individual_1.fitness < individual_2.fitness else individual_2, self.population)

    def _select_mutagen_indices(self, target_index):
        mutagen_indices = []
        possible_mutagen_indices = [i for i in range(
            self.population_size) if i is not target_index]
        _shuffle(possible_mutagen_indices)
        mutagen_indices = possible_mutagen_indices[0:self.number_of_mutagens]
        return mutagen_indices

    def _calculate_mutagen_value(self, mutagen_indices, genotype_index):

        mutagen_values = [self.population[mutagen_indices[i]].genotype[genotype_index]
                          for i in range(self.number_of_mutagens)]
        # TODO: update to handle different types of mutations
        return sum([self.F*(mutagen_values[i]-mutagen_values[i+1])
                    for i in range(self.number_of_mutagens-1)])

    def _generate_genotype_for_trial(self, target_index, dimensions, mutagen_indices):
        target = self.population[target_index]
        D = _randint(0, dimensions)
        return [self._calculate_mutagen_value(mutagen_indices, genotype_index) if _random(
        ) <= self.CR or genotype_index == D else target.genotype[genotype_index] for genotype_index in range(dimensions)]

    def _selection(self, trial, target):
        return trial if trial.fitness < target.fitness else target

    def _crossover(self, target_index):
        mutagen_indices = self._select_mutagen_indices(target_index)
        trial = self._initialize_individual()
        trial.genotype = self._generate_genotype_for_trial(
            target_index, trial.dimensions, mutagen_indices)
        trial.calculate_fitness()
        return trial

    def _evolve_generation(self):
        next_generation = []
        for target_index in range(self.population_size):
            target = self.population[target_index]

            trial = self._crossover(target_index)
            next_generation.append(self._selection(trial, target))

        self.population = next_generation

    def _evolve_population(self):
        for _ in range(self.generations):
            self._evolve_generation()
            self.history.append(self._get_best_individual().fitness)

    def search(self):
        self._validate_instance()
        self._initialize_population()
        self._evolve_population()
        print("Best individual: ", self._get_best_individual().genotype)

    def plot_history(self):
        _plt.plot(self.history)
        _plt.show()
