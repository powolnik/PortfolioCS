# 🎮 GAME DESIGN DOCUMENT

## Inicjatywa Awatara

### Wersja 1.1 | Uwzględniono uwagi

---

> **Tagline:** *Gdy kod sam siebie nie napisze, a rekruter ma za dużo czasu.*

---

## 1. 📋 Streszczenie Wykonawcze

**Inicjatywa Awatara** to interaktywna symulacja rekrutacyjna typu sandbox, w której gracz (rekruter) zarządza zachowaniem autonomicznego awatara-programisty. Zadaniem rekrutera jest prezentacja projektów (terminali) poprzez sterowanie zachowaniem awatara, który — pozornie pomocny — ma własne zdanie, poziom motywacji i tendencję do bycia... nieco rozespanym.

### Unikalne Cechy Produktu

| Cecha | Opis |
|-------|------|
| **Autonomia NPC** | Awatar działa sam, gdy rekruter nic nie robi |
| **Dwa tryby prezentacji** | Aktywny (gracz steruje) / Autonomiczny (auto-showcase) |
| **System irytacji** | Poziom motywacji wpływa na dialogi i zachowanie |
| **Złośliwości rekrutera** | Tryb "sabotażysty" — testowanie cierpliwości awatara |
| **Symulator korpo** | Satyryczne przedstawienie procesu rekrutacji IT |

---

## 2. 🎯 Cel Gry i Warunki Zwycięstwa

### 2.1. Cel Gry

**Dla Rekrutera:** Pokazać wszystkie projekty (terminale) w jak najkrótszym czasie, utrzymując awatara w stanie produktywnym (motywacja > 0).

**Dla Awatara:** Przetrwać rekrutację bez utraty godności i motywacji.

### 2.2. Warunki Zwycięstwa

Rekruter wygrywa, gdy:

- ✅ Odwiedzi **wszystkie terminale** przynajmniej raz
- ✅ Awatar zachowa motywację **> 0** do końca sesji
- ✅ Czas sesji jest mniejszy niż ustalony limit **LUB** przy najniższym czasie

### 2.3. Warunki Przegranej

Rekruter przegrywa, gdy:

- ❌ Motywacja awatara spadnie do **0** — awatar wychodzi z pokoju
- ❌ Rekruter nie odwiedzi żadnego terminala przez **120 sekund** (timeout)
- ❌ Awatar "zbuntuje się" — osiągnie krytyczny poziom irytacji 3x z rzędu

### 2.4. System Punktacji

$$Score = (10000 \times \frac{odwiedzone\_terminale}{total\_terminale}) - (czas\_w\_sekundach \times 10) + (motywacja\_końcowa \times 5)$$

---

## 3. 🏗️ Architektura Stanów Awatara

### 3.1. Typy Zachowań — Kluczowa Distynkcja

To jest **kluczowe rozróżnienie** w mechanice gry:

| Scenariusz | Zachowanie Awatara |
|------------|-------------------|
| **Gracz steruje normalnie** | Awatar wykonuje komendy nawigacyjne (`/next`, `/prev`, `/goto`) i prezentuje projekty |
| **Gracz NIE PRZESZKADZA** | Awatar automatycznie prezentuje kolejne projekty w normalnym tempie |
| **Gracz NIC NIE ROBI przez 5s** | Awatar przechodzi w AUTO_SHOWCASE (z irytacją) |
| **Gracz PRZESZKADZA aktywnie** | Awatar reaguje złośliwością, traci motywację |

### 3.2. Diagram Stanów

```
                              ┌─────────────────┐
                              │   AUTO_IDLE     │
                              │ (domyślny start)│
                              └────────┬────────┘
                                       │ komenda nawigacyjna
                                       ▼
                    ┌──────────────────────────────────────┐
                    │          AKTYWNA PREZENTACJA         │
                    │  (gracz steruje: /next, /prev, etc.) │
                    └──────────────┬───────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
  │   MOVING    │          │ PRESENTING  │          │  IDLE       │
  │  (do celu)  │          │ (terminal)  │          │ (czekanie)  │
  └──────┬──────┘          └──────┬──────┘          └──────┬──────┘
         │                         │                         │
         │                         │          5s bez komendy │
         │                         │                         ▼
         │                         │               ┌─────────────────┐
         │                         │               │ AUTO_SHOWCASE   │
         │                         │               │ "sam pokażę..." │
         │                         │               └────────┬────────┘
         ▼                         │                        │
  ┌─────────────┐                 │                        │
  │ SABOTAGED   │◀────────────────┴────────────────────────┘
  │(złośliwość) │
  └─────────────┘
         │
         ▼
  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
  │MANUAL_STOP  │          │  CONFUSED   │          │  BREAKPOINT │
  │   (/stop)   │          │  (/ghost)   │          │ (motyw=0)   │
  └─────────────┘          └─────────────┘          └─────────────┘
```

### 3.3. Tryby Prezentacji — Szczegółowo

#### 3.3.1. Tryb Aktywny (Gracz Steruje)

```
Warunek:     Gracz używa komend nawigacyjnych (/next, /prev, /goto)
Stan:        MOVING → PRESENTING
Zachowanie:  Awatar idzie do wskazanego terminala i prezentuje go
Dialog:      "O, ten projekt jest niezły! Spójrz!" / "Wracamy? Ok."
Motywacja:   +10 za dotarcie, +15 za ukończenie prezentacji
```

#### 3.3.2. Tryb Autonomiczny (Gracz Nie Przeszkadza)

```
Warunek:     Gracz wydał komendę nawigacyjną, ale NIE używa złośliwości
Stan:        PRESENTING → AUTO_PRESENT (płynnie)
Zachowanie:  Po zakończeniu prezentacji, awatar SAM idzie do następnego terminala
Prędkość:    Normalna (200 jednostek/s)
Dialog:      "Ten był fajny! Mam jeszcze jeden..." / "Kolejny projekt!"
Motywacja:   Stabilna (brak decay), +10/+15 jak normalnie
```

#### 3.3.3. Tryb Auto-Showcase (Gracz Nic Nie Robi)

```
Warunek:     Gracz NIE wydał żadnej komendy przez 5 sekund
Stan:        AUTO_SHOWCASE
Zachowanie:  Awatar sam znajduje najbliższy nieodwiedzony terminal i idzie do niego
Prędkość:   +20% szybciej (210 jednostek/s) — "pokazuje inicjatywę"
Dialog:      "Dobra, nie to nie, sam pokażę ci coś fajnego!"
Motywacja:   +8 za dotarcie (mniej niż normalnie, bo inicjatywa sama)
             -1 za każde użycie auto-showcase (irytacja: "sam muszę")
```

---

## 4. 🗺️ Mapa i Środowisko

### 4.1. Układ Mapy

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    [P1]                                                      │
│     ○                                                        │
│         ╲                    [P3]                           │
│          ╲                     ○                            │
│           ╲   ═══════          │                            │
│            ╲       ↑           │          [P5]              │
│    [P2]      ║    Awatar       │           ○                │
│     ○        ║       ♟️         │                            │
│              ║                  │                           │
│           ═══╩════              │           ═══════          │
│              [P4]               │               ↑           │
│               ○                 │          [P6]             │
│                                              ○               │
│                                                              │
│    ┌────────────────────────────────────────────────┐       │
│    │  UI: Motywacja [████████░░] 75%  |  Czas: 00:45 │       │
│    └────────────────────────────────────────────────┘       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 4.2. Parametry Środowiska

| Parametr | Wartość |
|----------|---------|
| Liczba terminali | 6 (skalowalne: 4-12) |
| Wymiary mapy | 1920×1080 jednostek (scaled) |
| Domyślna prędkość awatara | 200 jednostek/s |
| Prędkość auto-showcase | 240 jednostek/s (+20%) |
| Odległość interakcji z terminalem | 50 jednostek |
| Czas prezentacji terminala | 5-15 sekund (auto-skip po 15s) |
| Timeout do auto-showcase | 5 sekund bez komendy |

---

## 5. ⚙️ System Nawigacji i Komendy

### 5.1. Algorytm Wyboru Celu

```python
def calculate_target():
    """
    Wybierz następny terminal
    """
    
    if state == CONFUSED:
        # Szukaj na oślep (ghost_mode)
        return random_position_on_map()
    
    # Znajdź nieodwiedzone terminale
    unvisited = get_unvisited_terminals()
    
    if len(unvisited) == 0:
        # Wszystkie odwiedzone — zostań w miejscu
        return None
    
    # Znajdź 3 najbliższe
    candidates = sorted(unvisited, key=distance)[:3]
    
    # 80% szansa na najbliższy, 20% na losowy z top 3
    if random() < 0.8:
        return candidates[0]
    else:
        return random.choice(candidates)
```

### 5.2. Komendy Nawigacyjne

| Komenda | Składnia | Efekt | Opóźnienie |
|---------|----------|-------|------------|
| `/next` | `/next` | Przerwij, idź do następnego na liście | 0.5s |
| `/prev` | `/prev` | Wróć do poprzedniego terminala | 0.5s |
| `/random` | `/random` | Losowy terminal (z animacją "kręcenia") | 1.5s |
| `/stop` | `/stop` | Natychmiastowe zatrzymanie | 0s |
| `/goto [n]` | `/goto 3` | Idź do konkretnego terminala | 0.5s |
| `/present` | `/present` | Zacznij prezentację bieżącego terminala | 0s |

### 5.3. Dialogi Komend Nawigacyjnych

```
/next    → "O, ten też jest niezły! Lecimy!"
/prev    → "Wracamy? Ok, pokażę ci jeszcze raz."
/random  → "Kostka mówi... terminal numer [X]!"
/stop    → "Okej, okej. Stoję. Ale się nie nudzę..."
/goto    → "Skok do [X]? W drogę!"
/present → "A więc oglądasz! No to patrz..."
```

### 5.4. Zachowanie Automatyczne

#### Gdy Gracz Nie Przeszkadza (po komendzie nawigacyjnej):

```
Po zakończeniu prezentacji terminala:
┌─────────────────────────────────────────────────────────────┐
│  Sprawdź: czy gracz aktywował złośliwość w ciągu 10s?      │
│                                                             │
│  NIE (gracz nie przeszkadza):                               │
│    → Awatar SAM idzie do następnego terminala              │
│    → Dialog: "Mam jeszcze jeden projekt..."                │
│    → Motywacja: stabilna                                    │
│                                                             │
│  TAK (gracz przeszkadza):                                   │
│    → Awatar ZATRZYMUJE się                                  │
│    → Czeka na dalsze komendy                                │
│    → Dialog: "Więc tak czy owak..."                         │
└─────────────────────────────────────────────────────────────┘
```

#### Gdy Gracz Nic Nie Robi (5 sekund bez komendy):

```
Awatar: "Dobra, nie to nie, sam pokażę ci coś fajnego!"
→ Przechodzi w stan AUTO_SHOWCASE
→ Zwiększa prędkość o 20%
→ Wybiera najbliższy nieodwiedzony terminal
→ Idzie i prezentuje (z mniejszym bonusem motywacji)
```

---

## 6. 😈 System Złośliwości (Sabotażu)

### 6.1. Klasyfikacja Złośliwości

| Typ | Nazwa | Wymagania | Efekt | Czas trwania |
|-----|-------|-----------|-------|--------------|
| **Fizyczny** | Mouse Trap | kliknięcie+hold | Wierzganie nogami | do puszczenia |
| **Fizyczny** | Laser Point | kursor na ekranie | 20% szansa na gonienie | 3s lub do wyjścia |
| **Destrukcyjny** | `/low_bandwidth` | komenda | Slow-motion + "LOADING..." | 10s |
| **Destrukcyjny** | `/invert_controls` | komenda | Bieg w przeciwną stronę | 8s |
| **Destrukcyjny** | `/ghost_mode` | komenda | Terminale niewidzialne | do `/reveal` |
| **Destrukcyjny** | `/sudo_reboot` | komenda | Reset stanu do IDLE | jednorazowo |
| **Środowiskowy** | Zmiana grawitacji | komenda | Chodzenie po suficie | 15s |
| **Środowiskowy** | Kradzież kawy | kliknięcie na ☕ | Brak bonusu | jednorazowo |

### 6.2. Kluczowa Zasada: Awatar Nie Przeszkadza = Awatar Prezentuje

To jest **fundamentalna zasada balansu**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    WPŁYW ZŁOŚLIWOŚCI                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BRAK ZŁOŚLIWOŚCI (przez 10s po komendzie):                    │
│  ├─ Awatar automatycznie prezentuje kolejne projekty           │
│  ├─ Brak utraty motywacji                                      │
│  └─ +10/+15 motywacji za prezentację                          │
│                                                                 │
│  AKTYWNA ZŁOŚLIWOŚĆ:                                            │
│  ├─ Awatar PRZERYWA prezentację                                │
│  ├─ Traci motywację (-3 do -20)                                │
│  ├─ Dialogi irytacji                                           │
│  └─ Potrzebuje nowej komendy nawigacyjnej                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3. Szczegółowe Mechaniki Złośliwości

#### 6.3.1. Mouse Trap (Pułapka na Mysz)

```
Warunek:     Rekruter kliknięcie + przytrzymanie na awatarze
Stan:        TRAPPED
Animacja:    Wierzganie nogami, ramiona w górze
Dialog:      "Puść mnie! Deadliny gonią!"
Obrona:      Brak (można tylko czekać)
Koszt:       -5 motywacji (tylko raz na 10 sekund)
Konsekwencja: Przerywa prezentację, awatar czeka na kolejne komendy
```

#### 6.3.2. Laser Point

```
Warunek:     Kursor myszy na ekranie podczas ruchu
Szansa:      20% przy każdym ruchu
Stan:        CHASING_CURSOR
Animacja:    Bieg ku kursotowi, "miau miau"
Dialog:      "Złap to! Błyszczy!"
Czas:        3 sekundy LUB do "złapania" kursora
Po czasie:   Powrót do RECALCULATING_PATH
Koszt:       -3 motywacji
```

#### 6.3.3. `/low_bandwidth`

```
Warunek:     Komenda rekrutera
Stan:        SLOW_MOTION
Prędkość:    50 jednostek/s (normalnie: 200)
Animacja:    Ciągnięcie za sobą napisu "LOADING... 25%"
Dialog:      "Przepraszam, mam wolne łącze... szukaj wujka Google..."
Czas:        10 sekund
Obrona:      /speedup (przyspiesza o 5 sekund, -3 motywacji)
Koszt:       -8 motywacji
```

#### 6.3.4. `/invert_controls`

```
Warunek:     Komenda rekrutera
Stan:        INVERTED
Sterowanie:  Każdy ruch = przeciwny kierunek
Animacja:    "Walczenie" z kierunkiem, przekręcanie się
Dialog:      "Coś jest nie tak! Kierunek odwrotny! Przepraszam!"
Czas:        8 sekund
Obrona:      Poczekaj aż minie (lub -8 motywacji, by zignorować)
Koszt:       -8 motywacji
```

#### 6.3.5. `/ghost_mode`

```
Warunek:     Komenda rekrutera
Stan:        GHOST_MODE
Efekt:       Wszystkie terminale stają się NIEWIDZIALNE
Awatar:      Stan CONFUSED - biega losowo, szuka celu
Dialog:      "Gdzie ja to wrzuciłem?! Mapuję na ślepo..."
Obrona:      Komenda /reveal (odkrywa wszystkie terminale, -5 motywacji)
Czas:        Do odwołania
Koszt:       -10 motywacji (za dezorientację)
```

#### 6.3.6. `/sudo_reboot`

```
Warunek:     Komenda rekrutera
Efekt:       Natychmiastowy reset stanu:
             - Awatar teleportuje się do centrum mapy
             - Zapomina aktualny cel
             - Przechodzi w stan IDLE
             - Traci postęp prezentacji
Animacja:    Ekran błyska, "reboot: system OK"
Dialog:      "...Gdzie jestem? Co robiłem? Czy był lunch?"
Koszt:       -20 motywacji (duży sabotaż!)
Obrona:      Brak
```

#### 6.3.7. Zmiana Grawitacji (`/gravity_flip`)

```
Warunek:     Komenda rekrutera
Stan:        CEILING_WALKER
Efekt:       Awatar chodzi po górnej krawędzi okna gry
Ścieżka:     Droga do terminali wydłuża się 2.5x
Dialog:      "Pierwszy na suficie! Patrzajcie, nie spadam!"
Czas:        15 sekund
Obrona:      Poczekaj lub /gravity_restore
Koszt:       -12 motywacji
```

#### 6.3.8. Kradzież Kawy

```
Warunek:     Rekruter kliknie na kubek ☕ przed awatarem
Efekt:       Awatar nie dostaje bonusu +15 motywacji
Dialog:      "Kto wypił moją kawę?! To był mój paliwo-kod!"
Awatar:      Jeśli awatar dotrze pierwszy: "+15! Jutro będzie lepiej!"
```

---

## 7. 📉 System Motywacji

### 7.1. Definicja

| Parametr | Wartość |
|----------|---------|
| Maksimum | 100 |
| Start | 75 |
| Minimum (breakpoint) | 0 |
| Decay w `/stop` | -2/sekunda |

### 7.2. Modyfikatory Motywacji

| Akcja | Zmiana |
|-------|--------|
| **Pozytywne** | |
| Odwiedzenie terminala | +10 |
| Ukończenie prezentacji | +15 |
| Awatar sam prezentuje (auto) | +8 |
| **Negatywne** | |
| Komenda `/stop` | -2/sekunda |
| Mouse Trap (pierwsze złapanie) | -5 |
| Laser Point | -3 |
| `/low_bandwidth` | -8 |
| `/invert_controls` | -8 |
| `/ghost_mode` | -10 |
| `/sudo_reboot` | -20 |
| Zmiana grawitacji | -12 |
| Auto-showcase (gdy gracz nic nie robi) | -1 za każde użycie |
| `/stop` powyżej 30 sekund | Dodatkowe -10 (karencja) |

### 7.3. Progi i Zachowania

| Poziom | Punkty | Zachowanie awatara |
|--------|--------|-------------------|
| 😎 **OPTYMISTA** | 80-100 | Pełen entuzjazm, dodatkowe dialogi, "szybki tryb" |
| 🙂 **ZRELASKOWANY** | 60-79 | Normalne zachowanie, automatyczna prezentacja |
| 😐 **ZNUŻONY** | 40-59 | Narzekanie, wolniejsze ruchy (-20% prędkości) |
| 😤 **ZIRYTOWANY** | 20-39 | Otwarte wkurzenie, odmowa niektórych komend |
| 😫 **ZWYCIAŻONY** | 5-19 | Ble, pisanie CV "na boku", ignorowanie rekrutera |
| 💀 **BREAKPOINT** | 0 | Koniec gry — awatar wychodzi |

---

## 8. 💬 System Reakcji i Dialogów

### 8.1. Matryca Reakcji

| Poziom | Akcja | Tekst Awatara |
|--------|-------|---------------|
| **OPTYMISTA** (80+) | Postawienie przeszkody | "Haha, niezły trick! Ale i tak to skompiluję!" |
| | Laser Point | "O, błyskotka! Daj, daj!" |
| | /invert_controls | "Hej, reversed! Lubię wyzwania!" |
| **ZRELASKOWANY** (60-79) | Postawienie przeszkody | "Oj, obejdę. Professional move." |
| | Mouse Trap | "Hej hej, bez dotykania!" |
| | /low_bandwidth | "A taki fajny projekt... i taki wolny net." |
| **ZNUŻONY** (40-59) | Kliknięcie w postać | "Ej, to nieprofesjonalne. Skupmy się na kodzie." |
| | Przeszkoda na drodze | "Serio? Muszę to obejść? Mógłbyś pomóc." |
| | /ghost_mode | "Czemu wszystko znikło? To ty? Przestań." |
| **ZIRYTOWANY** (20-39) | /block | "Poważnie? Kolejny roadblock? Czuję się jak w korpo..." |
| | /invert_controls | "Przepraszam, że żyję! Nie musisz utrudniać!" |
| | Zmiana grawitacji | "Okej, super. Zmieniam planetę. Czemu nie." |
| **ZWYCIAŻONY** (5-19) | Jakakolwiek złośliwość | "Idę na L4. Powodzenia z szukaniem innego seniora." |
| | Próba komendy | "*wzdycha* Rób co chcesz. I tak już mi to obojętne." |

### 8.2. Dialogi Automatycznej Prezentacji

Gdy awatar sam (bez przeszkadzania) prezentuje kolejne projekty:

```
→ Po zakończeniu prezentacji, bez nowej komendy:
   "Ten projekt był niezły, co? Mam jeszcze jeden..."
   "Chcesz zobaczyć kolejny? Bo ja mam ich więcej!"
   "Idziemy dalej? Ok, prowadzę!"

→ Po 2. z rzędu automatycznej prezentacji:
   "Widzę, że ci się podoba! Spokojnie, mam więcej..."
   "*uśmiech* Nie ma za co, to moja praca!"

→ Po 3.+ automatycznej prezentacji:
   "Ok, kto tu naprawdę pracuje? 😏"
   "Sam sobie radzę, co? Mogę być twoim asystentem AI!"
```

---

## 9. 🔄 Pętla Gry (Game Loop) — Zaktualizowana

### 9.1. Flowchart z Uwzględnieniem Trybów

```
┌─────────────────────────────────────────────────────────────────┐
│                         START GRY                               │
│                      (motywacja: 75)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OCZEKIWANIE NA INPUT                      │
│                  (stan: IDLE, czas: odliczanie 5s)             │
│                                                                 │
│    ┌──────────────────────────────────────────────────────┐    │
│    │  INPUT OTRZYMANY                                      │    │
│    └───────────────────┬──────────────────────────────────┘    │
│                        │                                        │
│        ┌───────────────┼───────────────┐                       │
│        ▼               ▼               ▼                       │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                    │
│   │NAWIGACJA│    │ZŁOŚLIWOŚĆ│    │ /stop   │                    │
│   │/next,   │    │sabotage │    │ -2/s    │                    │
│   │/prev... │    │-motywacja    │         │                    │
│   └────┬────┘    └────┬────┘    └────┬────┘                    │
│        │              │              │                          │
│        ▼              ▼              ▼                          │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                    │
│   │ MOVING  │    │SABOTAGED│    │STOPPED  │                    │
│   │→PRESENTS│    │irytacja │    │ -2/s    │                    │
│   └────┬────┘    └────┬────┘    └────┬────┘                    │
│        │              │              │                          │
│        │    10s BEZ   │              │                          │
│        │   ZŁOŚLIWOŚCI│              │                          │
│        │    (auto-    │              │                          │
│        │    present)  │              │                          │
│        │              │              │                          │
│        ▼              ▼              ▼                          │
│   ┌─────────────────────────────────────────┐                  │
│   │         PRESENTING TERMINALA            │                  │
│   │     +10 motywacji (dojście)             │                  │
│   │     +15 motywacji (ukończenie)          │                  │
│   └────────────────────┬────────────────────┘                  │
│                        │                                        │
│         10s bez nowej  │komendy PO prezentacji                 │
│                        │                                        │
│                        ▼                                        │
│   ┌─────────────────────────────────────────┐                  │
│   │   AUTO_PRESENT → następny terminal      │◀── Równolegle:   │
│   │   (gdy gracz NIE przeszkadza)           │    Jeśli 5s       │
│   └────────────────────┬────────────────────┘    bez KOMENDY:  │
│                        │                          AUTO_SHOWCASE │
│                        │                          (-1 motywacji)│
└────────────────────────┼────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │ <6/6      │   │ MOTYWACJA │   │  TIMEOUT  │
   │ odwiedzone│   │   ≤ 0     │   │  120s     │
   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
         │               │               │
         ▼               ▼               ▼
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │   WIN     │   │   LOSE    │   │   LOSE    │
   │  +SCORE   │   │  GAME OVER│   │  TIMEOUT  │
   └───────────┘   └───────────┘   └───────────┘
```

### 9.2. Pseudo-code

```python
def game_loop():
    state = IDLE
    no_command_timer = 0
    time_since_last_sabotage = 0
    consecutive_auto_presents = 0
    
    while motywacja > 0:
        
        command = get_player_input()
        
        if command:
            no_command_timer = 0
            
            if command in NAVIGATION_COMMANDS:
                # Gracz steruje normalnie
                execute_navigation(command)
                state = MOVING
                
                # Reset licznika sabotażu
                time_since_last_sabotage = 0
                
            elif command in SABOTAGE_COMMANDS:
                # Gracz przeszkadza!
                apply_sabotage(command)
                state = SABOTAGED
                time_since_last_sabotage = 0
                consecutive_auto_presents = 0  # reset auto
                
            elif command == "/stop":
                state = STOPPED
                
        else:
            # Brak komendy
            no_command_timer += delta_time
            time_since_last_sabotage += delta_time
            
            # === KLUCZOWE: Sprawdź tryb ===
            
            if state == PRESENTING or state == MOVING:
                # Gracz był aktywny, teraz nic nie robi
                
                if time_since_last_sabotage > 10.0:
                    # 10s bez złośliwości = może auto-prezentować
                    if no_command_timer > 2.0:  # 2s przerwy między projektami
                        auto_present_next()
                        consecutive_auto_presents += 1
                        
            elif no_command_timer >= 5.0:
                # 5s absolutnie bez żadnej komendy
                # = auto-showcase (mniej optymalne)
                start_auto_showcase()
                consecutive_auto_presents = 0
        
        # Aktualizacja stanu
        update_avatar_state()
        update_motivation(delta_time)
        
        # Sprawdzenie warunków końca
        if all_terminals_visited():
            return WIN
            
        if motywacja <= 0:
            return LOSE
            
        if time_elapsed > 120 and no_interaction:
            return TIMEOUT
```

---

## 10. 📊 Balancing i Parametry

### 10.1. Domyślne Wartości

| Parametr | Wartość | Uwagi |
|----------|---------|-------|
| Liczba terminali | 6 | Można skalować 4-12 |
| Czas na terminal | 8s (średnio) | Zależy od interact time |
| Motywacja startowa | 75 | Powyżej średniej |
| Decay /stop | -2/s | Ostrożnie! |
| Timeout do auto-showcase | 5s | Brak jakiejkolwiek komendy |
| Okno auto-prezentacji | 10s | Czas bez sabotażu po komendzie |
| Bonus terminal (normalny) | +10 (+15 za ukończenie) | Gdy gracz steruje |
| Bonus terminal (auto-present) | +8 (+12 za ukończenie) | Gdy awatar sam prezentuje |
| Bonus terminal (auto-showcase) | +5 (+8 za ukończenie) | Gdy gracz nic nie robi |

### 10.2. Progi Automatycznej Prezentacji

| Warunek | Efekt |
|---------|-------|
| Komenda nawigacyjna + 10s bez sabotażu | Awatar sam prezentuje następny projekt |
| 5s absolutnie bez komendy | Awatar przechodzi w auto-showcase (irytacja) |

---

## 11. ✅ Checklist Implementacyjny — Zaktualizowany

```
_CORE MECHANICS_
□ System stanów awatara (3 tryby prezentacji)
□ Rozróżnienie: sterowanie / auto-present / auto-showcase
□ Pathfinding (NN + losowość)
□ Komendy nawigacyjne (/next, /prev, /random, /stop, /goto)
□ Auto-present po 10s bez sabotażu
□ Auto-showcase po 5s absolutnie bez komendy

_SABOTAGE SYSTEM_
□ Mouse Trap (kliknięcie+hold)
□ Laser Point (20% szansa)
□ /low_bandwidth
□ /invert_controls
□ /ghost_mode + /reveal
□ /sudo_reboot
□ Zmiana grawitacji
□ Kradzież kawy

_UI/AUDIO_
□ Pasek motywacji
□ Liczniki (czas, terminale)
□ Input komend
□ Dialogi (chmurki)
□ Tryb auto-present dialogi
□ Lo-fi muzyka
□ SFX interakcji

_GAME LOOP_
□ Warunki zwycięstwa
□ Warunki przegranej
□ Scoring system (3 poziomy bonusu)
□ Reset gry
```

---

## 12. 📝 Podsumowanie Kluczowych Zmian

### 12.1. Co Zostało Poprawione

| Element | Przed | Po |
|---------|-------|-----|
| **Brak rozróżnienia trybów** | Jeden tryb auto | 3 odrębne zachowania |
| **Auto-showcase** | Jedyny tryb autonomiczny | Tylko gdy gracz NIC nie robi |
| **Brak "próżni"** | Po komendzie — czekanie | Auto-present gdy nie przeszkadzasz |
| **Motywacja za auto** | Jeden bonus | 3 poziomy zależne od trybu |

### 12.2. Diagram Zależności Trybów

```
                    GRACZ WYDAJE KOMENDĘ
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
     NAWIGACJA       ZŁOŚLIWOŚĆ        /stop
           │               │               │
           ▼               ▼               ▼
      MOVING          SABOTAGED        STOPPED
           │               │               │
           │      10s BEZ  │               │
           │     ZŁOŚLIWOŚCI               │
           │               │               │
           ▼               ▼               ▼
    PRESENTING    ◄──── IRYTACJA
           │
           │ 10s bez sabotażu
           │ (gracz nie przeszkadza)
           ▼
    AUTO_PRESENT
    (awatar sam idzie dalej)
           │
           │ 5s bez JAKIEJKOLWIEK komendy
           ▼
    AUTO_SHOWCASE
    ("sam pokażę...")
```

---

**Dokument przygotowany do dalszego rozwoju.**
*Wersja: 1.1 | Data: 2025 | Status: Gotowy do implementacji*