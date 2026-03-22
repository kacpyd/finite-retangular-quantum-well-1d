# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 13:59:33 2026

@author: kacpe
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

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

def wykres(a, V0, opis):
    eps = np.linspace(-V0 + 1e-4, -1e-4, 4000)
    
    fe = Feven(eps, a, V0)
    fo = Fodd(eps, a, V0)

    fe[np.abs(fe) > 20] = np.nan
    fo[np.abs(fo) > 20] = np.nan
    
    plt.figure(figsize=(10,6))
    plt.plot(eps, fe, label="Feven")
    plt.plot(eps, fo, label="Fodd")
    plt.axhline(0, color="black")
    plt.xlabel("eps")
    plt.ylabel("wartosc funckji")
    plt.title(f"{opis}  (a = {a}, V0 = {V0})")
    plt.grid(True)
    plt.legend()
    plt.show()

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

def znajdz_poziomy(a, V0):
    # siatka energii w zakresie dozwolonym dla stanów związanych
    eps = np.linspace(-V0 + 1e-4, -1e-4, 4000)

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

    # pierwszy poziom – parzysty
    E1 = bisekcja(lambda e: Feven(e, a, V0), *przedzialy_even[0])
    # drugi poziom – nieparzysty
    E2 = bisekcja(lambda e: Fodd(e, a, V0), *przedzialy_odd[0])

    return E1, E2

def blad(param):
    a, V0 = param
    try:
        E1, E2 = znajdz_poziomy(a, V0)
    except:
        # jeśli coś pójdzie źle (np. brak korzeni), zwracamy duży błąd
        return [10, 10]

    return [
        E1 + 0.5,      # chcemy E1 = -0.5
        E2 + 0.125     # chcemy E2 = -0.125
    ]

# punkt startowy z treści zadania
start = [3.0, 1.0]

rozw = fsolve(blad, start)

a_opt, V0_opt = rozw
print("Dopasowane parametry:")
print("a =", a_opt)
print("V0 =", V0_opt)

E1, E2 = znajdz_poziomy(a_opt, V0_opt)
print("Poziomy energii dla dopasowanej studni:")
print("E1 =", E1, " (cel: -0.5)")
print("E2 =", E2, " (cel: -0.125)")

# opcjonalnie: wykres dla dopasowanej studni
wykres(a_opt, V0_opt, "Studnia dopasowana do H (n=1,2)")
