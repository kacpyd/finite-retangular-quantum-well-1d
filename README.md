# Prostokątna skończona studnia kwantowa
## Stacjonarne równanie Schrödingera w jednym wymiarze

Projekt wykonany w Pythonie dotyczący numerycznego rozwiązania stacjonarnego równania Schrödingera dla prostokątnej skończonej studni kwantowej w jednym wymiarze.

## Zawartość projektu

### `src/studnia4.py`
Program realizujący zadanie 1:
- tablicowanie funkcji `F_even(ε)` i `F_odd(ε)`,
- wyznaczanie miejsc zerowych odpowiadających poziomom energii,
- analiza różnych parametrów studni potencjału,
- generowanie wykresów.

### `src/atom1.py`
Program realizujący zadanie 2 oraz zadanie zaawansowane 1:
- dopasowanie parametrów studni kwantowej do pierwszych poziomów energii atomu wodoru,
- analiza zgodności wyników,
- automatyczne znajdowanie parametrów studni.

### `src/atom2.py`
Program realizujący zadanie zaawansowane 2:
- wyznaczanie funkcji własnych,
- rysowanie funkcji własnych oraz `|ψ|²`,
- obserwację tunelowania kwantowego.

## Wymagania

Projekt korzysta z bibliotek:
- NumPy
- SciPy
- Matplotlib

Instalacja:
```bash
pip install -r requirements.txt
