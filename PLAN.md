# 🗺️ Plan Implementacji: `gra-strona-portfolio`

## 🚀 Status Projektu: **W TOKU**
- [x] **Faza 1: Python Kernel** (Zakończona)
- [x] **Faza 2: C++ Integration** (Zakończona/Fundamenty gotowe)
- [ ] **Faza 3: AI Avatar & Feedback** (W kolejce)

---

## 🏗️ Faza 1: Python Kernel (Fundamenty)
*Cel: Stworzenie działającej strony CLI z podstawowymi informacjami.*

- [x] **Konfiguracja Backend/Frontend:** FastAPI (`backend/main.py`) + Pygbag (`engine/main.py`).
- [x] **Kernel Terminala:** Implementacja parsera komend w Pythonie (klasa `TerminalAI`).
- [x] **Komendy P0:**
    - [x] `whoami`, `ls`, `contact`, `help`, `clear`, `status`.
- [x] **Renderer CRT:** Podstawowa wizualizacja Pygame-ce.

## ⚙️ Faza 2: C++ Integration (Moduły Zewnętrzne)
*Cel: Uruchamianie zewnętrznych modułów C++ wewnątrz środowiska Pythona.*

- [x] **Pipeline Emscripten:** Skrypt `scripts/compile_cpp.sh` i `shell.html` gotowe.
- [x] **WASM Loader:** Integracja `platform.window.frame_online` w `engine/main.py`.
- [x] **Obsługa Komend Rozszerzonych:**
    - [x] `run [project]` - przełączanie widoku na moduł WASM (iframe bridge).
    - [x] `cat [file]` - szkielet obsługi wyświetlania kodu.
- [x] **Demo Moduł:** Mock `hello_wasm` gotowy do testów integracyjnych.

## 🤖 Faza 3: AI Avatar & Feedback (Mechaniki Gry)
*Cel: Dodanie interaktywności i "duszy" systemowi.*

- [ ] **Logika Ruchu Avatara:** Autonomiczny byt (ASCII/Sprite) poruszający się po terminalu.
- [ ] **System Stabilności (`SYSTEM_STABILITY`):** 
    - [ ] Wpływ na płynność animacji.
    - [ ] Dynamiczne glitche wizualne.
- [ ] **Interakcja z Rekruterem:**
    - [ ] Reakcje AI na komendy "ataku" (np. `kill -9`, `memory_leak`).
    - [ ] System inteligentnych logów systemowych (`[INFO]`, `[WARNING]`).

## 🎨 Faza 4: Polish & Optymalizacja
- [ ] **Efekty CRT:** Shadery (scanlines, distortion).
- [ ] **Mobile Support:** Wirtualna klawiatura.
- [ ] **SEO Layer:** Statyczny HTML z treścią CV dla botów.
