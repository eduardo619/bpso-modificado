import numpy as np, random, pandas as pd
from math import sin, pi
import datetime

class BPSOModificado(object):
    
    def __init__(self, nParticulas: int, nDimensiones: int, prcMutacion: float, vMin: float, vMax: float, nIteraciones:int):
        self._nparticulas = nParticulas
        self._ndimensiones = nDimensiones
        self._prcmutacion = prcMutacion
        self._vmin = vMin
        self._vmax = vMax
        self._niteraciones = nIteraciones

        self.V = np.empty(shape=(self._nparticulas, self._ndimensiones), dtype=float)
        self.G = np.empty(shape=(self._nparticulas, self._ndimensiones), dtype=float)
        self.X = np.empty(shape=(self._nparticulas, self._ndimensiones), dtype=int)
        self.P = np.empty(shape=(self._nparticulas, self._ndimensiones), dtype=int)
        self._r1 = random.random()
        self._r2 = random.random()
        self._w = 0.721
        self._c1 = 2
        self._c2 = 2
        self._g: int

    
    def Algoritmo(self):
        contador = 0
        
        data = {
            'INDICE':[],
            'INDICE DE G': [],
            'FORMA': [],
            'FITNESS': []
        }

        for i in range(self._nparticulas):
            for j in range(self._ndimensiones):
                self.V[i, j] = random.randrange(start=self._vmin, stop=self._vmax)

        self.G = self.V

        for i in range(self._nparticulas):
            for j in range(self._ndimensiones):
                self.X[i, j] = random.randint(0, 1)

        self.P = self.X

        while(self._niteraciones != 0):

            for i in range(self._nparticulas):
                if(self.Maximizar(self.X[i]) > self.Maximizar(self.P[i])):
                    for d in range(self._ndimensiones):
                        self.P[i, d] = self.X[i, d]
                
                g = i

                for j in range(self._nparticulas):
                    if(self.Maximizar(self.P[j]) > self.Maximizar(self.P[g])):
                        g = j

                for d in range(self._ndimensiones):
                    self.V[i, d] = self._w * self.V[i, d] + self._c1 * self._r1 * (self.P[i,d] - self.X[i, d]) + self._c2 * self._r2 * (self.P[g, d] - self.X[i, d])
                    self.G[i, d] = self.G[i, d] + self.V[i, d]

                    if random.random() < self._prcmutacion:
                        self.G[i, d] = -self.G[i, d]
                    
                    if random.random() < self.Sigmoide(self.G[i, d]):
                        self.X[i, d] = 1
                    else:
                        self.X[i, d] = 0

            data['INDICE'].append(contador)
            data['INDICE DE G'].append(g)
            data['FORMA'].append(self.toString(self.P[g]))
            data['FITNESS'].append(self.Maximizar(self.P[g]))

            contador = contador + 1
            self._niteraciones = self._niteraciones -1

        df = pd.DataFrame(data, columns = ['INDICE', 'INDICE DE G', 'FORMA', 'FITNESS'])
        
        df.to_csv('bpso-modificado{0}{1}{2}.csv'.format(random.randint(0,9), random.randint(0,9), random.randint(0,9)))

    def toString(self, valor: list):
        return str("{0}{1}{2}{3}{4}{5}{6}{7}".format(valor[0], valor[1], valor[2], valor[3], valor[4], valor[5], valor[6], valor[7]))


    def Maximizar(self, valor:list) -> float:
        binario = int("{0}{1}{2}{3}{4}{5}{6}{7}".format(valor[0], valor[1], valor[2], valor[3], valor[4], valor[5], valor[6], valor[7]), base=2)
        return sin(pi * binario / 256)


    def Sigmoide(self, velocidad: float):
        return 1 / (1 + np.exp(-velocidad))


obj = BPSOModificado(10, 8, 0.4, -6.0, 6.0, 500)
obj.Algoritmo()

##