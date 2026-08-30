from neat import config, chromosome, genome
import sys
import pickle
from cart_pole import CartPole

if len(sys.argv) > 1:
    # load genome
    try:
        fp = open(sys.argv[1], 'rb')
    except IOError:
        print("Filename: '" + sys.argv[1] + "' not found!")
        sys.exit(0)
    else:
        c = pickle.load(fp)
        fp.close()
else:
    print("Loading default winner chromosome file")
    try:
        fp = open('winner_chromosome', 'rb')
    except IOError:
        print("Winner chromosome not found!")
        sys.exit(0)
    else:
        c = pickle.load(fp)
        fp.close()

# load settings file
config.load('cpExp_config')
print("Loaded genome:")
print(c)
# starts the simulation
simulator = CartPole([c], markov=False)
simulator.run(testing=True)
