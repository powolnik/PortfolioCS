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
        self.logs = ["[INFO] Kernel 0.9.8 initialized.", "[INFO] System stability: 100%", "[HINT] Type 'sudo help' for commands."]
        
        # Avatar state
        self.avatar_pos = [400, 300]
        self.path = [[100, 100], [700, 100], [700, 500], [100, 500]]
        self.path_index = 0
        self.base_speed = 3.0
        self.current_speed = self.base_speed
        self.glitch_timer = 0
        self.is_rebooting = False

    def add_log(self, text, type="INFO"):
        prefix = f"[{type}] "
        # Glitch effect for logs at low stability
        if self.stability < 40 and random.random() > 0.7:
            text = "".join([c if random.random() > 0.3 else random.choice("!@#$%^&*") for c in text])
        
        self.logs.append(f"{prefix}{text}")
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

        if self.is_killed and base_cmd != "reboot":
            self.add_log("SYSTEM HALTED. PERMISSION DENIED.", "ERROR")
            return

        if base_cmd in ["help", "sudo help"]:
            self.add_log("PORTFOLIO: whoami, ls, cat [proj], run [proj], status, contact", "SYSTEM")
            self.add_log("ATTACK: inject_latency, spawn_deadlock, memory_leak, kill -9", "WARNING")
        elif base_cmd == "whoami":
            self.add_log("Role: Senior Software Engineer / C++ Specialist", "INFO")
        elif base_cmd == "ls":
            self.add_log("/projects: [hello_wasm, path_tracer, sorting_visualizer]", "INFO")
        elif base_cmd == "status":
            self.add_log(f"STABILITY: {self.stability}% | UPTIME: {pygame.time.get_ticks()//1000}s", "INFO")
        elif base_cmd == "inject_latency":
            self.stability = max(0, self.stability - 15)
            self.current_speed *= 0.6
            self.add_log("Unauthorized interference! Latency injected.", "WARNING")
        elif base_cmd == "spawn_deadlock":
            self.stability = max(0, self.stability - 20)
            self.add_log("Critical drop! Deadlock detected in Sector 7.", "ERROR")
        elif base_cmd == "memory_leak":
            self.stability = max(0, self.stability - 10)
            self.add_log("Memory leak detected. System bloating...", "WARNING")
        elif base_cmd == "kill -9" or (base_cmd == "kill" and "-9" in args):
            self.stability = 0
            self.is_killed = True
            self.add_log("KERNEL PANIC: Process killed by SIGKILL.", "ERROR")
        elif base_cmd == "reboot":
            self.stability = 100
            self.is_killed = False
            self.current_speed = self.base_speed
            self.add_log("Rebooting... System restored.", "SYSTEM")
        elif base_cmd == "run":
            if not args:
                self.add_log("run: missing project name", "ERROR")
            else:
                project = args[0]
                if project in ["hello_wasm", "path_tracer", "sorting_visualizer"]:
                    self.add_log(f"Launching {project} in display buffer...", "INFO")
                    if platform:
                        platform.window.frame_online(f"/static/wasm/{project}/index.html")
                else:
                    self.add_log(f"Module '{project}' not found.", "ERROR")
        elif base_cmd == "clear":
            self.logs = []
        else:
            self.add_log(f"Unknown command: {cmd}", "ERROR")

    def update_avatar(self):
        if self.is_killed: return

        # Target point logic
        target = self.path[self.path_index]
        dx = target[0] - self.avatar_pos[0]
        dy = target[1] - self.avatar_pos[1]
        dist = (dx**2 + dy**2)**0.5

        # Speed depends on stability
        move_speed = self.current_speed * (self.stability / 100.0)
        
        if dist < move_speed:
            self.avatar_pos = list(target)
            self.path_index = (self.path_index + 1) % len(self.path)
        else:
            self.avatar_pos[0] += (dx / dist) * move_speed
            self.avatar_pos[1] += (dy / dist) * move_speed

    async def main_loop(self):
        import pygame
        import math
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("monospace", FONT_SIZE)
        self.clock = pygame.time.Clock()

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

            self.update_avatar()
            self.screen.fill(COLOR_BG)

            # Draw Avatar (AI Kernel)
            avatar_color = COLOR_TEXT
            if self.stability < 30:
                avatar_color = (random.randint(100, 255), 0, 0)
            elif self.stability < 60:
                avatar_color = (200, 200, 0)
            
            # Avatar visual (square + glitch lines)
            pygame.draw.rect(self.screen, avatar_color, (self.avatar_pos[0]-10, self.avatar_pos[1]-10, 20, 20))
            if self.stability < 100 and not self.is_killed:
                for _ in range(int((100 - self.stability) / 10)):
                    lx = self.avatar_pos[0] + random.randint(-30, 30)
                    ly = self.avatar_pos[1] + random.randint(-30, 30)
                    pygame.draw.line(self.screen, avatar_color, (self.avatar_pos[0], self.avatar_pos[1]), (lx, ly), 1)

            # Draw Logs
            for i, log in enumerate(self.logs):
                color = COLOR_TEXT
                if "[ERROR]" in log: color = (255, 50, 50)
                elif "[WARNING]" in log: color = (255, 200, 0)
                elif "[SYSTEM]" in log: color = (0, 200, 255)
                
                text_surf = self.font.render(log, True, color)
                self.screen.blit(text_surf, (10, 10 + i * (FONT_SIZE + 2)))
            
            # CRT Scanline effect (simplified)
            for y in range(0, 600, 4):
                pygame.draw.line(self.screen, (0, 0, 0, 50), (0, y), (800, y))

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
