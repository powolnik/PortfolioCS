# Game Design Document: `gra-strona-portfolio.pl` (Python/C++ Edition)
---

## 📋 Podstawowe Informacje o Projekcie
| Wartość | Opis |
|---------|------|
| **Tytuł** | `gra-strona-portfolio` - AI Terminal Portfolio |
| **Platforma** | Web (Python + WebAssembly), optymalizowane pod przeglądarki desktopowe (styl terminala) |
| **Cel Główny** | Prezentacja umiejętności programistycznych w C++ i Pythonie poprzez interaktywny terminal AI, który "hostuje" projekty i reaguje na działania rekrutera. |
| **Docelowi Odbiorcy** | Rekruterzy techniczni (C++/Python), programiści systemowi, entuzjaści Cyberpunka/CLI. |

---

## 🎮 Koncepcja Główna: "The Kernel AI"
Użytkownik (Rekruter) nie wchodzi na zwykłą stronę, ale uzyskuje dostęp do "Terminala Deweloperskiego". Głównym bohaterem jest **Avatar AI (Kernel)** – byt napisany w Pythonie, który wizualizuje postępy w pracy twórcy.

Rekruter może:
1.  Wpisywać komendy CLI do interakcji ze światem.
2.  Próbować "przeciążyć system" (zakłócanie avatara), co testuje stabilność kodu.
3.  Uruchamiać **Moduły Zewnętrzne** (projekty w C++ skompilowane do WASM) bezpośrednio wewnątrz terminala.

---

## 🧰 Szczegółowe Mechaniki Gry

### 1. Wizualizacja: Terminal CRT / AI
| Element | Opis |
|---------|------|
| **Styl Wizualny** | Estetyka Retro-Terminala (fonty monospaced, efekty scanline, kolorystyka Matrix Green / Cyber Cyan). |
| **Interfejs** | Konsola tekstowa jako główny sposób nawigacji + okno wizualizacji graficznej (Pygame-ce). |
| **Avatar** | Zglitchowany byt ASCII lub minimalistyczny sprite, który reaguje na logi systemowe. |

---

### 2. System Stabilności Procesu (Zamiast Energii)
Avatar posiada parametr `SYSTEM_STABILITY` (0-100%). Zakłócenia rekrutera to "procesy obciążające":
| Akcja Rekrutera | Skutek |
|----------------------|---------------|
| `inject_latency` | Spowolnienie ruchu avatara. |
| `spawn_deadlock` | Postawienie przeszkody na ścieżce (ściana). |
| `memory_leak` | Obszar spowalniający ("błoto"). |
| `kill -9` | Natychmiastowe zatrzymanie avatara (wymaga "rebootu"). |

---

### 3. Interakcja i Komendy
Głównym narzędziem jest parser komend w Pythonie.
| Komenda | Działanie |
|---------|-----------|
| `ls /projects` | Lista dostępnych projektów (C++ / Python). |
| `run [project_name]` | Uruchamia projekt C++ jako moduł WebAssembly w dedykowanym oknie. |
| `status` | Wyświetla parametry życiowe systemu i statystyki "ataków" rekrutera. |
| `sudo help` | Wyświetla listę dostępnych komend z uprawnieniami administratora. |
| `clear` | Czyści bufor terminala. |

---

### 4. Odpowiedzi Avatara (AI Logs)
Logi systemowe generowane w Pythonie pełnią rolę komentarzy:
- *[INFO] Project "PathTracer_CPP" loaded successfully into memory.*
- *[WARNING] Unauthorized interference detected in Sector 7. Recalculating path...*
- *[ERROR] Critical stability drop! Please optimize your behavior, Human.*

---

### 5. Prezentacja Projektów C++
Kluczowy punkt portfolio. Projekty napisane w C++ (np. silniki graficzne, algorytmy, narzędzia systemowe) są prezentowane jako:
- **Live Demo:** Skompilowane przez Emscripten do WASM i osadzone w ramce terminala.
- **Source View:** Możliwość podejrzenia fragmentów kodu `header/source` bezpośrednio w konsoli komendą `cat`.

---

## 💻 Techniczne Wymagania (Python & C++ Stack)
1.  **Backend/Web:** **FastAPI (Python)** – obsługa routingu i serwowanie plików.
2.  **Frontend Logic:** **PyScript** lub **Pygbag** (Python działający w przeglądarce przez WebAssembly).
3.  **Grafika/Avatar:** **Pygame-ce** – lekki silnik do wizualizacji avatara 2D.
4.  **Projekty C++:** Kompilowane za pomocą **Emscripten (WASM/C++)**, integrowane z główną stroną.
5.  **Brak Javy/JavaScript:** Całość logiki biznesowej i prezentacyjnej oparta na Pythonie, z minimalnym, niezbędnym glue-codem JS generowanym automatycznie przez narzędzia Pythonowe.

---

## 🚀 Proces Tworzenia
### Faza 1: Python Kernel
- Konfiguracja FastAPI i Pygbag.
- Stworzenie parsera komend tekstowych w Pythonie.
- Implementacja renderera terminala CRT.

### Faza 2: C++ Integration
- Przygotowanie rurociągu (pipeline) Emscripten dla projektów C++.
- Stworzenie systemu "ładowania modułów" WASM do strony w Pythonie.

### Faza 3: AI Avatar & Feedback
- Implementacja logiki ruchu avatara w Pygame-ce.
- System dynamicznych logów (komentarzy) w zależności od akcji rekrutera.

---

## 📝 Podsumowanie
`gra-strona-portfolio` w wersji Python/C++ to manifest techniczny. Zamiast standardowych narzędzi webowych, projekt wykorzystuje technologie natywne i systemowe (WASM, C++, Python), udowadniając kompetencje autora w inżynierii oprogramowania, a nie tylko w prostym tworzeniu stron WWW.
