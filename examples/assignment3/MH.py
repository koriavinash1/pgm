import sys
import numpy as np
sys.path.append('../..')
from pgm.inference.MetropolisHastings import MH
from matplotlib import pyplot as plt

def Gamma(theta, k = 1):
    def G(k):
        if k <= 0: return 1
        elif k == 0.5: return np.pi **0.5
        return k*G(k-1)
    def distribution(x):
        x = np.abs(x)
        return (x**(k-1))*np.exp(-x/theta)/((theta**k) * G(k))    
    return distribution


def proposalDistribution(sigma=2):
    """
        Describes example proposal distribution
        considers gaussion distribution with fixed sigma
        as the mean keeps changing it's made an inner function argument
    """
    def QDistribution(param = 0):
        return lambda x: (1/(((2*np.pi)**0.5) * sigma))*np.exp(-((x-param)**2)/ (sigma**2))

    return QDistribution, lambda x: np.random.normal(x, sigma)


# ==========================================
function = Gamma(theta=5.5, k=1)
proposalDistribution, proposalSampler = proposalDistribution()

MH = MH(function, 100, proposalDistribution, proposalSampler)
nMontecarlo = 10500

x = np.linspace(-20, 20, 500)
fx = function(x)

for _ in range(nMontecarlo):
    next(MH.sampler())

sampledvalues = np.array(MH.x_seq)[500:]
plt.plot(x, fx, 'b--', linewidth=2.0)
plt.hist(sampledvalues, 500, density=True, facecolor='g', alpha=0.7, linewidth=0)
plt.legend(['target pdf', 'sampled histogram'])
plt.show()

plt.plot(sampledvalues, linewidth=2.0)
plt.ylim(-20.0, 20.0)
plt.show()


