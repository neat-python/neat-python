from population import *
from nn import *
from config import Config
if Config.nn_allow_recurrence:
    from genome import *
else:
    from genome_feedforward import *