import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# ============================
#  Funkcje fizyczne
# ============================

def k_fun(eps, V0):
    # Wektor falowy wewnątrz studni: k = sqrt(2(E + V0))
    return np.sqrt(2*(eps + V0))

def kappa_fun(eps):
    # Wektor zanikający poza studnią: kappa = sqrt(-2E)
    return np.sqrt(-2*eps)

def Feven(eps, a, V0):
    # Równanie dla stanów parzystych: tan(k a/2) = kappa/k
    k = k_fun(eps, V0)
    kap = kappa_fun(eps)
    return np.sin(k*a/2) - (kap/k) * np.cos(k*a/2)

def Fodd(eps, a, V0):
    # Równanie dla stanów nieparzystych: tan(k a/2) = -k/kappa
    k = k_fun(eps, V0)
    kap = kappa_fun(eps)
    return np.sin(k*a/2) + (k/kap) * np.cos(k*a/2)

# ============================
#  Rysowanie wykresów Feven i Fodd
# ============================

def wykres(a, V0, opis):
    # Zakres energii dla stanów związanych: (-V0, 0)
    eps = np.linspace(-V0 + 1e-4, -1e-4, 4000)
    
    fe = Feven(eps, a, V0)
    fo = Fodd(eps, a, V0)

    # Usuwamy wartości bardzo duże, aby wykres był czytelny
    fe[np.abs(fe) > 20] = np.nan
    fo[np.abs(fo) > 20] = np.nan
    
    plt.figure(figsize=(10,6))
    plt.plot(eps, fe, label="Feven")
    plt.plot(eps, fo, label="Fodd")
    plt.axhline(0, color="black")
    plt.xlabel("eps")
    plt.ylabel("wartosc funkcji")
    plt.title(f"{opis}  (a = {a}, V0 = {V0})")
    plt.grid(True)
    plt.legend()
    plt.show()

# ============================
#  Metoda bisekcji
# ============================

def bisekcja(f, a, b , tol = 1e-10, max_itter = 100):
    # Sprawdzamy, czy funkcja zmienia znak na przedziale
    if f(a) * f(b) >= 0:
        raise ValueError('Funkcja nie zmienia znaku na przedziale!')
        
    for i in range(max_itter):
        c = (a + b) / 2  # punkt środkowy
        
        # Warunek zakończenia: wartość bliska 0 lub bardzo mały przedział
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        
        # Wybór podprzedziału, w którym funkcja zmienia znak
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2

# ============================
#  Automatyczne znajdowanie poziomów energii
# ============================

def znajdz_poziomy(a, V0):
    # Siatka energii w zakresie dozwolonym dla stanów związanych
    eps = np.linspace(-V0 + 1e-4, -1e-4, 4000)

    fe = Feven(eps, a, V0)
    fo = Fodd(eps, a, V0)

    # Funkcja pomocnicza: wykrywa przedziały, gdzie funkcja zmienia znak
    def znajdz_korzenie(f_vals):
        roots = []
        for i in range(len(f_vals)-1):
            # Pomijamy NaN-y
            if np.isnan(f_vals[i]) or np.isnan(f_vals[i+1]):
                continue
            # Zmiana znaku → potencjalny korzeń
            if f_vals[i] * f_vals[i+1] < 0:
                roots.append((eps[i], eps[i+1]))
        return roots

    # Przedziały dla stanów parzystych i nieparzystych
    przedzialy_even = znajdz_korzenie(fe)
    przedzialy_odd  = znajdz_korzenie(fo)

    # Pierwszy poziom – parzysty
    E1 = bisekcja(lambda e: Feven(e, a, V0), *przedzialy_even[0])
    # Drugi poziom – nieparzysty
    E2 = bisekcja(lambda e: Fodd(e, a, V0), *przedzialy_odd[0])

    return E1, E2

# ============================
#  Funkcja błędu dla fsolve
# ============================

def blad(param):
    a, V0 = param
    try:
        # Obliczamy poziomy energii dla zadanych parametrów
        E1, E2 = znajdz_poziomy(a, V0)
    except:
        # Jeśli nie uda się znaleźć korzeni → zwracamy duży błąd
        return [10, 10]

    # Zwracamy różnice względem wartości docelowych
    return [
        E1 + 0.5,      # chcemy E1 = -0.5
        E2 + 0.125     # chcemy E2 = -0.125
    ]

# ============================
#  Rozwiązywanie układu równań
# ============================

# Punkt startowy z treści zadania
start = [3.0, 1.0]

# fsolve szuka parametrów a i V0, które dają zadane poziomy energii
rozw = fsolve(blad, start)

a_opt, V0_opt = rozw
print("Dopasowane parametry:")
print("a =", a_opt)
print("V0 =", V0_opt)

# Obliczamy poziomy energii dla znalezionych parametrów
E1, E2 = znajdz_poziomy(a_opt, V0_opt)
print("Poziomy energii dla dopasowanej studni:")
print("E1 =", E1, " (cel: -0.5)")
print("E2 =", E2, " (cel: -0.125)")

# Wykres dla dopasowanej studni
wykres(a_opt, V0_opt, "Studnia dopasowana do H (n=1,2)")
