import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# ============================
# Funkcje fizyczne
# ============================

def k_fun(eps, V0):
    # Wektor falowy wewnątrz studni: k = sqrt(2(E + V0))
    return np.sqrt(2 * (eps + V0))

def kappa_fun(eps):
    # Wektor zanikający poza studnią: kappa = sqrt(-2E)
    return np.sqrt(-2 * eps)

def Feven(eps, a, V0):
    # Równanie dla stanów parzystych
    k = k_fun(eps, V0)
    kap = kappa_fun(eps)
    return np.sin(k * a / 2) - (kap / k) * np.cos(k * a / 2)

def Fodd(eps, a, V0):
    # Równanie dla stanów nieparzystych
    k = k_fun(eps, V0)
    kap = kappa_fun(eps)
    return np.sin(k * a / 2) + (k / kap) * np.cos(k * a / 2)

# ============================
# Rysowanie wykresów Feven i Fodd
# ============================

def wykres(a, V0, opis):
    eps = np.linspace(-V0 + 1e-4, -1e-4, 4000)

    fe = Feven(eps, a, V0)
    fo = Fodd(eps, a, V0)

    # Usuwamy bardzo duże wartości dla czytelności wykresu
    fe = fe.copy()
    fo = fo.copy()
    fe[np.abs(fe) > 20] = np.nan
    fo[np.abs(fo) > 20] = np.nan

    plt.figure(figsize=(10, 6))
    plt.plot(eps, fe, label="Feven")
    plt.plot(eps, fo, label="Fodd")
    plt.axhline(0, color="black")
    plt.xlabel("eps")
    plt.ylabel("wartość funkcji")
    plt.title(f"{opis}  (a = {a:.6f}, V0 = {V0:.6f})")
    plt.grid(True)
    plt.legend()
    plt.show()

# ============================
# Metoda bisekcji
# ============================

def bisekcja(f, a, b, tol=1e-10, max_iter=100):
    fa = f(a)
    fb = f(b)

    if not np.isfinite(fa) or not np.isfinite(fb):
        raise ValueError("Niepoprawne wartości funkcji na krańcach przedziału.")

    if fa * fb >= 0:
        raise ValueError("Funkcja nie zmienia znaku na przedziale.")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if not np.isfinite(fc):
            raise ValueError("Niepoprawna wartość funkcji w środku przedziału.")

        if abs(fc) < tol or (b - a) / 2 < tol:
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return (a + b) / 2

# ============================
# Automatyczne znajdowanie poziomów energii
# ============================

def znajdz_przedzialy_zmiany_znaku(eps, f_vals):
    przedzialy = []

    for i in range(len(f_vals) - 1):
        y1 = f_vals[i]
        y2 = f_vals[i + 1]

        # Pomijamy NaN i inf
        if not np.isfinite(y1) or not np.isfinite(y2):
            continue

        # Zmiana znaku => przedział zawiera miejsce zerowe
        if y1 * y2 < 0:
            przedzialy.append((eps[i], eps[i + 1]))

    return przedzialy

def znajdz_poziomy(a, V0):
    # Zakres energii stanów związanych
    eps = np.linspace(-V0 + 1e-4, -1e-4, 4000)

    fe = Feven(eps, a, V0)
    fo = Fodd(eps, a, V0)

    przedzialy_even = znajdz_przedzialy_zmiany_znaku(eps, fe)
    przedzialy_odd = znajdz_przedzialy_zmiany_znaku(eps, fo)

    poziomy = []

    # Korzenie dla stanów parzystych
    for p in przedzialy_even:
        E = bisekcja(lambda e: Feven(e, a, V0), *p)
        poziomy.append(("even", E))

    # Korzenie dla stanów nieparzystych
    for p in przedzialy_odd:
        E = bisekcja(lambda e: Fodd(e, a, V0), *p)
        poziomy.append(("odd", E))

    # Sortowanie energetyczne: od najbardziej ujemnych do najmniej ujemnych
    poziomy.sort(key=lambda x: x[1])

    return poziomy

# ============================
# Funkcja błędu dla fsolve
# ============================

def blad(param):
    a, V0 = param

    # Parametry fizyczne muszą być dodatnie
    if a <= 0 or V0 <= 0:
        return [10, 10]

    try:
        poziomy = znajdz_poziomy(a, V0)
    except Exception:
        return [10, 10]

    # Musimy mieć co najmniej dwa poziomy
    if len(poziomy) < 2:
        return [10, 10]

    E1 = poziomy[0][1]
    E2 = poziomy[1][1]

    return [
        E1 + 0.5,    # chcemy E1 = -0.5
        E2 + 0.125   # chcemy E2 = -0.125
    ]

# ============================
# Rozwiązywanie układu równań
# ============================

start = [3.0, 1.0]

rozw = fsolve(blad, start)
a_opt, V0_opt = rozw

print("Dopasowane parametry:")
print("a  =", a_opt)
print("V0 =", V0_opt)

# ============================
# Wyznaczenie wszystkich poziomów
# ============================

poziomy = znajdz_poziomy(a_opt, V0_opt)

print("\nPoziomy energii dla dopasowanej studni:")
for i, (typ, E) in enumerate(poziomy, start=1):
    print(f"E{i} = {E:.10f}   ({typ})")

# Dodatkowo wypiszmy dwa pierwsze poziomy i porównanie z celem
if len(poziomy) >= 2:
    E1 = poziomy[0][1]
    E2 = poziomy[1][1]

    print("\nPorównanie z wartościami docelowymi:")
    print(f"E1 = {E1:.10f}   (cel: -0.5)")
    print(f"E2 = {E2:.10f}   (cel: -0.125)")

# Jeśli istnieje trzeci poziom, wypiszmy go osobno
if len(poziomy) >= 3:
    E3 = poziomy[2][1]
    print(f"E3 = {E3:.10f}")

# ============================
# Wykres dla dopasowanej studni
# ============================

wykres(a_opt, V0_opt, "Studnia dopasowana do H (n=1,2)")
