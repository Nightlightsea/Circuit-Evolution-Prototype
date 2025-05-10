class EvolutionConfig:
    def __init__(self):

        # ---Simulation Settings--- #
        self.GENERATIONS = 2000
        self.GEN_POOL = 30
        self.POPULATION = 100
        self.PENALTY = 0.80
        self.TOP_POPULATION = 0.2

        # ---Multithreading--- #
        self.MULTITHREADING = True
        self.CORES = 8

        # ---Circuit Settings--- #
        self.LANES = 4
        self.LANES_SIZE = 5
        self.INITIAL_GATE_AMOUNT = 5
        self.MINIMAL_GATE_AMOUNT = 2
        self.MAXIMAL_GATE_AMOUNT = 30

        # ---Mutations Settings--- #
        self.MUTATION_RATE = 0.2
        self.MUTATIONS_IN_GEN = 50

        # ---Crossover Settings--- #
        self.GENERATION_CROSSOVER = 50
        self.GENERATION_CROSSOVER_DURATION = 2
        self.CROSSOVER_IN_GEN = 5

        # ---Stuff--- #
        self.NEW_IN_GEN = 40
        self.COMPUTE_ROUNDS = 10