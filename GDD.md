# Game Design Document: `gra-strona-portfolio.pl`
---

## 📋 Podstawowe Informacje o Projekcie
| Wartość | Opis |
|---------|------|
| **Tytuł** | `gra-strona-portfolio` - Interaktywna Strona Portfolio w Formie Gry 2D |
| **Platforma** | Strona internetowa (oparta na silniku Phaser.js 3, kompatybilna z przeglądarkami mobilnymi i stacjonarnymi) |
| **Cel Główny** | Stworzenie interaktywnej wersji portfolio, która zastępuje statyczną podstronę grą, w której potencjalni rekruterzy mogą zanurzyć się w procesie prezentacji umiejętności, a jednocześnie sprawdzić, jak radzimy sobie z niespodziankami w pracy. |
| **Docelowi Odbiorcy** | Rekruterzy z branży IT/grafiki designerów, przyjaciele, rodzina oraz studenci chcący nauczyć się tworzyć interaktywne strony internetowe. |

---

## 🎮 Koncepcja Główna
Graczem jest potencjalny rekruter, który wchodzi na stronę portfolio. Przed nim otwiera się dwuwymiarowy świat, w którym porusza się Avatar Twórcy – reprezentacja autora portfolio. Avatar porusza się automatycznie po zaprojektowanej ścieżce, aby przedstawić poszczególne projekty z portfolio, umieszczone w różnych punktach mapy.

Rekruter ma możliwość:
1.  Zakłócania procesu prezentacji za pomocą myszki lub komend tekstowych
2.  Odbierania awatarpowi punktów energii
3.  Dotykania się do interakcji z autorem, który komentuje każde zakłócenie w czasie rzeczywistym

Głównym celem rekruty jest zobaczenie wszystkich projektów z portfolio, nawet mimo zakłóceń. Po zakończeniu prezentacji wyświetla się podsumowanie z statystykami wykonanych akcji zakłócających.

---

## 🧰 Szczegółowe Mechaniki Gry

### 1. Świat 2D Portfolio
| Element | Opis |
|---------|------|
| **Styl Wizualny** | Minimalistyczny flat design dopasowany do brandu autorskiego (możliwość dostosowania kolorów, czcionek i grafiki w panelu administracyjmnym twórcy). |
| **Struktura Świata** | **Terminal AI - Portfolio Structure**
