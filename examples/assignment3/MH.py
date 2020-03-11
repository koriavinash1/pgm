import sys
sys.path.append('../..')
from pgm.inference.MetropolisHastings import MH

complex_function = ''
burninT = ''
proposalDistribution = ''

MH = MH(complex_function, burninT = 100, proposalDistribution)
nMontecarlo = 1000
X = []

for i in range(nMontecarlo):
    X.append(MH.sampler())
