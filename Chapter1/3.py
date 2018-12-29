import math
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

# 3. Look in a neurobiology book for the full set of differential equations of the Hodgkin-Huxley model.
# Write a computer program that simulates an action potential

# Constants
# Na = Sodium
# K  = Potassium
# L  = Leakage

# Outside current applied to the nerve
I = 0.1  # mA?

# Capacitance of the membrane
cm = 0.01  # uF/cm^2

# Potential
e_na = 55.17  # mV
e_k = -72.14  # mV
e_l = -49.42  # mV

# Conductance
g_na = 1.2  # mS/cm^2
g_k = 0.36  # mS/cm^2
g_l = 0.003  # mS/cm^2

# time step and total length (in ms)
t = 25.0  # ms
dt = 0.04  # ms
size = int(t / dt)  # total size of loop/graph we are creating

timearr = np.arange(0, t + dt, dt)

# Permissivity values of m,n,h
def am(V): return float((0.1 * (V + 35)) / (1 - math.exp((-1.0 * (V + 35)) / 10)))
def an(V): return float((0.01 * (V + 50)) / (1 - math.exp((-1.0 * (V + 50)) / 10)))
def ah(V): return float(0.07 * math.exp(-0.05 * (V + 60)))
def bm(V): return float(4.0 * math.exp(-0.0556 * (V + 60)))
def bn(V): return float(0.125 * math.exp((-1.0 * (V + 60)) / 80))
def bh(V): return float(1.0 / (1.0 + math.exp(-0.1 * (V + 30))))

#Initial voltage of the membrane (-60 to -70 mV)
v_0 = -60.0 #mV

#Initial channel values for m,n,h
m_0 = am(v_0)/(am(v_0) + bm(v_0))
n_0 = an(v_0)/(an(v_0) + bn(v_0))
h_0 = ah(v_0)/(ah(v_0) + bh(v_0))

def getLine(appliedCurrent, subplotindex):
    I = appliedCurrent

    # arrays for graphing
    v = [0.0] * (size + 1)
    m = [0.0] * (size + 1)
    n = [0.0] * (size + 1)
    h = [0.0] * (size + 1)

    #set our initial values
    v[0] = v_0; m[0] = m_0; n[0] = n_0; h[0] = h_0

    for i in range(0, size):
        #solve for the m,n,h channel values each step, using euler method
        m[i + 1] = m[i] + dt * ((am(v[i])*(1-m[i]))-(bm(v[i]))*m[i])
        n[i + 1] = n[i]+ dt * ((an(v[i])*(1-n[i]))-(bn(v[i])*n[i]))
        h[i + 1] = h[i] + dt * ((ah(v[i])*(1-h[i]))-(bh(v[i])*h[i]))

        #get current conductance values
        gna = g_na * math.pow(m[i], 3) * h[i]
        gk = g_k * math.pow(n[i], 4)
        gl = g_l #gl doesn't change, will define here for verbosity

        #get current current values using g values just gathered
        Ina = gna * (v[i] - e_na)
        Ik = gk * (v[i] - e_k)
        Il = gl * (v[i] - e_l)

        #Finally, solve for our next voltage value
        v[i + 1] = v[i] + (dt * ((1.0/cm) * (I - (Ina + Ik + Il))))

    plt.subplot(4, 1, subplotindex)
    plt.ylabel("Voltage(mV)")
    plt.title("I = %f" % I)
    if subplotindex != 4:
        plt.plot(timearr, v, 'g-')
    else:
        plt.xlabel("Time(ms)")
        plt.plot(timearr, v, 'g-',)

if __name__ == "__main__":
    currentRange = np.arange(0.1, 1.1, 0.3)

    subplotindex = 1
    for i in currentRange:
        getLine(i, subplotindex)
        subplotindex += 1

    plt.show()