import numpy as np
import matplotlib.pyplot as plt

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
    plt.plot(eps, fo, label="Food")
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

def rozwiaz_przypadek(a, V0, opis, przedzialy_even, przedzialy_odd):
    print("\n======================")
    print(opis)
    print("a = ", a, "V0 = ", V0)
    
    wykres(a, V0, opis)
    
    print("\nStany parzyste:")
    for lewy, prawy in przedzialy_even:
        root = bisekcja(lambda e: Feven(e, a, V0), lewy, prawy)
        print(f"przedzial [{lewy}, {prawy}] ---> eps = {root}")
        
    print("\nStany nieparzyste:")
    for lewy, prawy in przedzialy_odd:
        root = bisekcja(lambda e: Fodd(e, a, V0), lewy, prawy)
        print(f"przedzial [{lewy}, {prawy}] ---> eps = {root}")
        
rozwiaz_przypadek(
    a = 8,
    V0 = 0.5,
    opis = "Studnia plytka i szeroka",
    przedzialy_even = [
        (-0.48, -0.4),
        (-0.15, -0.05)
        ],
    przedzialy_odd = [
        (-0.35, -0.28),
        ]
    )

rozwiaz_przypadek(
    a = 2,
    V0 = 10,
    opis = "Studnia posrednia",
    przedzialy_even = [
        (-9.7, -8.5),
        (-4.0, -2.4)
        ],
    przedzialy_odd = [
        (-7.5, -6.0),
        ]
    )

rozwiaz_przypadek(
    a = 1,
    V0 = 50,
    opis = "Studnia glęboka i wąska",
    przedzialy_even = [
        (-48.0, -43.0),
        (-23.0, -17.0)
        ],
    przedzialy_odd = [
        (-40.0, -33.0),
        (-5.0, -1.0)
        ]
    )
