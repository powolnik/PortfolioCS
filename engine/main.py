import asyncio
import sys
import random

# Konfiguracja kolorów i stylu
COLOR_BG = (13, 2, 8)
COLOR_TEXT = (0, 255, 65)
COLOR_SCANLINE = (0, 255, 65, 20)
COLOR_OBSTACLE = (100, 0, 0)
COLOR_SLOWZONE = (0, 60, 0)
FONT_SIZE = 20

class TerminalAI:
    def __init__(self):
        self.screen = None
        self.font = None
        self.clock = None
        self.stability = 100
        self.is_running = True
        self.is_killed = False
        self.input_buffer = ""
        self.logs = ["[INFO] Kernel initialized.", "[INFO] System stability: 100%", "[HINT] Type 'help' for commands."]
        self.avatar_pos = None
        self.avatar_target = None
        self.base_speed = 2.5
        self.current_speed = self.base_speed
        self.obstacles = []
        self.slow_zones = []

    def add_log(self, text):
        self.logs.append(text)
        if len(self.logs) > 18:
            self.logs.pop(0)

    def handle_command(self, cmd):
        import pygame
        try:
            import platform
        except ImportError:
            platform = None

        cmd = cmd.strip().lower()
        if not cmd: return
        
        parts = cmd.split(" ")
        base_cmd = parts[0]
        args = parts[1:]

        if base_cmd in ["help", "sudo help"]:
            self.add_log("> Available: whoami, contact, ls, status, cat [proj], run [proj], clear, reboot")
        elif base_cmd == "whoami":
            self.add_log("--- USER PROFILE ---")
            self.add_log("Role: Senior Software Engineer / C++ Specialist")
        elif base_cmd == "contact":
            self.add_log("--- CONNECTION ---")
            self.add_log("Email: contact@gra-strona-portfolio.pl")
        elif base_cmd in ["ls", "ls /projects"]:
            self.add_log("> /projects: [hello_wasm, path_tracer, sorting_visualizer]")
        elif base_cmd == "clear":
            self.logs = []
        elif base_cmd == "status":
            self.add_log(f"> SYSTEM_STATUS: {self.stability}% | KERNEL: Pygame-CE/WASM")
        elif base_cmd == "cat":
            if not args:
                self.add_log("[ERROR] cat: missing operand")
            else:
                self.add_log(f"[INFO] Reading {args[0]} source...")
                # In a real app, this would fetch from backend
                self.add_log("(Source view is partially implemented via FastAPI endpoint)")
        elif base_cmd == "run":
            if not args:
                self.add_log("[ERROR] run: missing project name")
            else:
                project = args[0]
                projects = ["hello_wasm", "path_tracer", "sorting_visualizer"]
                if project in projects:
                    self.add_log(f"[INFO] Launching module: {project}...")
                    if platform:
                        try:
                            # Using the frame_online function defined in index.html
                            url = f"/static/wasm/{project}/index.html"
                            platform.window.frame_online(url)
                            self.add_log(f"[INFO] {project} active in display buffer.")
                        except Exception as e:
                            self.add_log(f"[ERROR] Bridge failure: {e}")
                    else:
                        self.add_log("[WARNING] Running in local mode. No WASM bridge.")
                else:
                    self.add_log(f"[ERROR] Module '{project}' not found in /projects.")
        else:
            self.add_log(f"[ERROR] Unknown command: {cmd}")

    async def main_loop(self):
        import pygame
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.font = pygame.font.SysFont("monospace", FONT_SIZE)
            self.clock = pygame.time.Clock()
            self.avatar_pos = pygame.Vector2(400, 300)
            self.avatar_target = pygame.Vector2(400, 300)
        except Exception as e:
            print(f"Pygame init failed: {e}")
            return

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.handle_command(self.input_buffer)
                        self.input_buffer = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1]
                    else:
                        self.input_buffer += event.unicode

            self.screen.fill(COLOR_BG)
            for i, log in enumerate(self.logs):
                text_surf = self.font.render(log, True, COLOR_TEXT)
                self.screen.blit(text_surf, (10, 10 + i * (FONT_SIZE + 2)))
            
            # Input line
            pygame.draw.rect(self.screen, (10, 30, 10), (5, 565, 790, 30))
            pygame.draw.rect(self.screen, COLOR_TEXT, (5, 565, 790, 30), 1)
            prompt = "admin@kernel:~$ "
            input_text = f"{prompt}{self.input_buffer}"
            if (pygame.time.get_ticks() // 500) % 2 == 0: input_text += "_"
            input_surf = self.font.render(input_text, True, COLOR_TEXT)
            self.screen.blit(input_surf, (10, 570))
            
            pygame.display.flip()
            await asyncio.sleep(0)
            self.clock.tick(60)

if __name__ == "__main__":
    terminal = TerminalAI()
    asyncio.run(terminal.main_loop())
