# 🗺️ Plan Implementacji: `gra-strona-portfolio`

## 🏗️ Faza 1: Fundamenty (Terminal & Portfolio) - PRIORYTET: WYSOKI (P0)
*Cel: Stworzenie działającej strony CLI z podstawowymi informacjami.*

- [x] **Setup Środowiska:** Konfiguracja FastAPI (backend) oraz Pygbag (frontend Python/WASM).
- [x] **Kernel Terminala:** Implementacja parsera komend tekstowych w Pythonie (obsługa `stdin/stdout`).
- [x] **Komendy Portfolio (P0):**
    - [x] `whoami` - wyświetlanie profilu zawodowego.
    - [x] `ls /projects` - lista projektów.
    - [x] `contact` - dane kontaktowe.
    - [x] `help` - system pomocy.
    - [x] `clear` - czyszczenie ekranu.
- [x] **Podstawowy Avatar:** Minimalistyczny sprite/ASCII w oknie Pygame-ce reagujący na wpisywanie tekstu.
- [x] **SEO Layer:** Przygotowanie statycznego pliku HTML z treścią CV dla robotów wyszukiwarek.

## ⚙️ Faza 2: Integracja C++ & WASM - PRIORYTET: WYSOKI (P1)
*Cel: Uruchamianie zewnętrznych modułów C++ wewnątrz środowiska Pythona.*

- [ ] **Pipeline Emscripten:** Skonfigurowanie kompilacji projektów C++ do formatu `.wasm`.
- [ ] **WASM Loader:** Mechanizm w Pythonie (Pygbag) do dynamicznego ładowania i wywoływania modułów C++.
- [ ] **Komenda `run [proj]`:** Implementacja logiki przełączania widoku Pygame-ce na output modułu C++.
- [ ] **Pierwszy Moduł:** `Sorting_Visualizer` lub `Hello_Wasm` (test komunikacji C++ -> Browser).
- [ ] **Komenda `cat`:** Wyświetlanie kodu źródłowego projektów (na razie bez podświetlania).

## 🤖 Faza 3: Mechaniki Gry & AI - PRIORYTET: ŚREDNI (P1)
*Cel: Dodanie interaktywności i "duszy" systemowi.*

- [ ] **System Stabilności:** Implementacja zmiennej `SYSTEM_STABILITY` i jej wpływu na zachowanie avatara.
- [ ] **Komendy Ataku:** `inject_latency`, `spawn_deadlock`, `kill -9` - wpływ na stabilność.
- [ ] **AI Feedback:** Dynamiczne logi systemowe (`[INFO]`, `[ERROR]`) generowane w zależności od akcji użytkownika.
- [ ] **Glitche:** Wizualne efekty zakłóceń przy niskiej stabilności (zniekształcenia tekstu, zmiana kolorów).

## 🎨 Faza 4: Polish & Optymalizacja - PRIORYTET: NISKI (P2)
*Cel: Efekty "wow" i dopracowanie UX.*

- [ ] **CRT Shaders:** Dodanie shaderów GLSL (zakrzywienie ekranu, scanlines).
- [ ] **Syntax Highlighting:** Kolorowanie składni dla komendy `cat` (np. proste regexy).
- [ ] **Mobile Bridge:** Implementacja wirtualnej klawiatura dla urządzeń dotykowych.
- [ ] **CV Download:** Integracja generowania/pobierania PDF (`cv --download`).
- [ ] **Easter Eggs:** Komendy `matrix`, `cowsay`, ukryte logi.

---
## 📈 Status Projektu: **W TOKU**
- [x] GDD.md (Zaktualizowane)
- [x] PLAN.md (Zdefiniowany)
- [x] Faza 1 (Zakończona)
- [ ] Faza 2 (W kolejce)
