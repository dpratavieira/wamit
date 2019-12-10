import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style


def converte_np_array(x):
    if isinstance(x, list):
        a = np.array(x)
    elif isinstance(x, int):
        a = np.array([x])
    else:
        a = x
    return a


def seaspec(formulation, tp, hs, depth=100):
    g = 9.80665
    tp = converte_np_array(tp)
    hs = converte_np_array(hs)
    pi = np.pi
    w = np.linspace(2*np.pi/(tp.max()*10), 2*np.pi/(tp.min()/10), 5000)
    w = w[:, np.newaxis]
    
    if formulation == 'j2':
    	# JONSWAP SPECTRUM CAMPOS BASIN
        gama = 6.4*tp**-0.491
        sw = (2*pi)**-1*(5/16*hs**2*tp*((2*pi/tp)/w)**5*(1-0.287*np.log(gama))*np.exp(-1.25*(w/(2*pi/tp))**-4)*gama**np.exp(-((w-(2*pi/tp))/2/pi)**2/(2*((w<=(2*pi/tp))*0.07+(w>(2*pi/tp))*0.09)**2*((2*pi/tp)/2/pi)**2)))
        return sw, w
    
    if formulation == 'tma':
        # TMA SPECTRUM
        w_h = w*(depth/g)**(.5)
        coef_tma = np.zeros(w_h.shape)

        idx = w_h <= 1
        coef_tma[idx] = .5 * w_h[idx]**2

        idx = np.logical_and(w_h > 1, w_h <=2)
        coef_tma[idx] = 1 - .5 * (2 - w_h[idx])**2

        idx = w_h > 2
        coef_tma[idx] = 1

        gama = 6.4*tp**-0.491
        sw_aux = (2*pi)**-1*(5/16*hs**2*tp*((2*pi/tp)/w)**5*(1-0.287*np.log(gama))*np.exp(-1.25*(w/(2*pi/tp))**-4)*gama**np.exp(-((w-(2*pi/tp))/2/pi)**2/(2*((w<=(2*pi/tp))*0.07+(w>(2*pi/tp))*0.09)**2*((2*pi/tp)/2/pi)**2)))
        sw = sw_aux * coef_tma

        m0_aux = np.trapz(sw_aux, x=w, axis=0)
        m0_tma = np.trapz(sw, x=w, axis=0)

        sw2 = sw * (m0_aux / m0_tma)

        # plt.plot(w, sw_aux, 'b')
        # plt.plot(w, sw, 'r')
        # plt.plot(w, sw2, 'k')
        # plt.show(block = False)
        return sw2, w


def legenda(hs):
    hs = converte_np_array(hs)
    texto = []
    i = 0
    while i < len(hs):
        texto.append('Hs = %.3f m' % hs[i])
        i += 1
    return texto


style.use('tableau-colorblind10')
# ['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright',
# 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted',
# 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
# 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']

# Tp = np.array([10, 10, 10])
# Hs = np.array([2, 4, 3])
Tp = [10, 20]
Hs = [3, 2]
Sw1, w1 = seaspec('tma', Tp, Hs, 40)

Hs_check = 4 * np.sqrt(np.trapz(Sw1, x = w1, axis=0))

# print(Hs_check)
tx = legenda(Hs_check)
Tp = converte_np_array(Tp)
plt.plot(2*np.pi/w1, Sw1)
plt.xlim(0, 2*Tp.max())
plt.grid(True)
plt.legend(tx)
plt.show()
