# 🗺️ Plan Implementacji: `gra-strona-portfolio`

- [x] **Faza 3: AI Avatar & Feedback** (Zakończona)
- [ ] **Faza 4: Polish & Optymalizacja** (W toku)

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

- [x] **Logika Ruchu Avatara:** Autonomiczny byt podążający po ścieżce.
- [x] **System Stabilności (`SYSTEM_STABILITY`):**
    - [x] Wpływ na prędkość i wizualne glitche.
    - [x] Dynamiczne zniekształcenia logów.
- [x] **Interakcja z Rekruterem:**
    - [x] Obsługa komend ataku: `inject_latency`, `spawn_deadlock`, `memory_leak`, `kill -9`.
    - [x] System kolorowych logów systemowych i reakcji AI.

## 🎨 Faza 4: Polish & Optymalizacja
- [x] **Efekty CRT:** Optymalizacja scanlines, dodanie winiety (vignette) i glitchy stabilności.
- [ ] **Mobile Support:** Wirtualna klawiatura.
- [ ] **SEO Layer:** Statyczny HTML z treścią CV dla botów.


- [ ] **Efekty CRT:** Shadery (scanlines, distortion).
- [ ] **Mobile Support:** Wirtualna klawiatura.
- [ ] **SEO Layer:** Statyczny HTML z treścią CV dla botów.

    aider --model openrouter/deepseek/deepseek-r1:free --chat-mode architect --yes-always --cache-prompts --pretty --stream --fancy-input --dark-mode --no-show-model-warnings --watch-files
