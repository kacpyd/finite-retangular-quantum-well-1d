# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 20:52:11 2026

@author: kacpe
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# ============================
# 1. Funkcje fizyczne
# ============================

def k_fun(eps, V0):
    return np.sqrt(2*(eps + V0))

def kappa_fun(eps):
    return np.sqrt(-2*eps)

def Feven(eps, a, V0):
    k = k_fun(eps, V0)
    kap = kappa_fun(eps)
    return np.sin(k*a/2) - (kap/k) * np.cos(k*a/2)

def Fodd(eps, a, V0):
    k = k_fun(eps, V0)
    kap = kappa_fun(eps)
    return np.sin(k*a/2) + (k/kap) * np.cos(k*a/2)

# ============================
# 2. Bisekcja
# ============================

def bisekcja(f, a, b , tol = 1e-10, max_itter = 100):
    if f(a) * f(b) >= 0:
        raise ValueError('Funkcja nie zmienia znaku na przedziale!')
        
    for i in range(max_itter):
        c = (a + b) / 2
        
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2

# ============================
# 3. Znajdowanie wszystkich poziomów energii
# ============================

def znajdz_wszystkie_poziomy(a, V0):
    eps = np.linspace(-V0 + 1e-4, -1e-4, 6000)

    fe = Feven(eps, a, V0)
    fo = Fodd(eps, a, V0)

    def znajdz_korzenie(f_vals):
        roots = []
        for i in range(len(f_vals)-1):
            if np.isnan(f_vals[i]) or np.isnan(f_vals[i+1]):
                continue
            if f_vals[i] * f_vals[i+1] < 0:
                roots.append((eps[i], eps[i+1]))
        return roots

    przedzialy_even = znajdz_korzenie(fe)
    przedzialy_odd  = znajdz_korzenie(fo)

    poziomy = []

    for (l, p) in przedzialy_even:
        poziomy.append(bisekcja(lambda e: Feven(e, a, V0), l, p))

    for (l, p) in przedzialy_odd:
        poziomy.append(bisekcja(lambda e: Fodd(e, a, V0), l, p))

    poziomy.sort()
    return poziomy

# ============================
# 4. Dopasowanie studni do poziomów H: n=1,2
# ============================

def blad(param):
    a, V0 = param
    try:
        poziomy = znajdz_wszystkie_poziomy(a, V0)
    except:
        return [10, 10]

    if len(poziomy) < 2:
        return [10, 10]

    E1 = poziomy[0]
    E2 = poziomy[1]

    return [
        E1 + 0.5,      # cel: -0.5
        E2 + 0.125     # cel: -0.125
    ]

start = [3.0, 1.0]
a_opt, V0_opt = fsolve(blad, start)

print("Dopasowane parametry studni:")
print("a =", a_opt)
print("V0 =", V0_opt)

poziomy = znajdz_wszystkie_poziomy(a_opt, V0_opt)
print("Poziomy energii:", poziomy)

# ============================
# 5. Funkcja falowa ψ(x)
# ============================

def psi_x(x, E, a, V0, parity):
    k = k_fun(E, V0)
    kap = kappa_fun(E)
    x = np.array(x)

    psi = np.zeros_like(x)

    inside = np.abs(x) <= a/2
    outside = ~inside

    if parity == 'even':
        psi[inside] = np.cos(k * x[inside])
        C = np.cos(k * a/2)
        psi[outside] = C * np.exp(-kap * (np.abs(x[outside]) - a/2))

    elif parity == 'odd':
        psi[inside] = np.sin(k * x[inside])
        C = np.sin(k * a/2)
        psi[outside] = np.sign(x[outside]) * C * np.exp(-kap * (np.abs(x[outside]) - a/2))

    return psi

# ============================
# 6. Rysowanie ψ(x) i ψ(x)²
# ============================

def rysuj_stan(a, V0, E, parity, opis):
    x = np.linspace(-2*a, 2*a, 2000)

    psi = psi_x(x, E, a, V0, parity)
    psi2 = psi**2

    plt.figure(figsize=(10,6))

    # schemat studni
    V = np.zeros_like(x)
    V[np.abs(x) <= a/2] = -V0
    V[np.abs(x) > a/2] = 0
    plt.fill_between(x, V, V.min() - 0.2*V0, color='lightgray', alpha=0.3)

    offset = -V0/2
    scale = V0/3

    plt.plot(x, offset + scale*psi, label="ψ(x)")
    plt.plot(x, offset + scale*psi2, label="ψ(x)²")

    plt.axvline(-a/2, color='k', linestyle='--', alpha=0.5)
    plt.axvline(a/2, color='k', linestyle='--', alpha=0.5)

    plt.title(opis + f"\nE = {E:.4f}, parity = {parity}")
    plt.xlabel("x")
    plt.ylabel("energia / amplituda (umowne jednostki)")
    plt.legend()
    plt.grid(True)
    plt.show()

# ============================
# 7. Rysowanie tylko istniejących stanów
# ============================

if len(poziomy) >= 1:
    rysuj_stan(a_opt, V0_opt, poziomy[0], 'even', "Stan podstawowy")

if len(poziomy) >= 2:
    rysuj_stan(a_opt, V0_opt, poziomy[1], 'odd', "Pierwszy stan wzbudzony")

if len(poziomy) >= 3:
    rysuj_stan(a_opt, V0_opt, poziomy[2], 'even', "Drugi stan wzbudzony")
else:
    print("Studnia ma tylko dwa stany związane — brak trzeciego poziomu.")