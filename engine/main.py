import pygame
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
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("AI Terminal Kernel")
        self.font = pygame.font.SysFont("monospace", FONT_SIZE)
        self.clock = pygame.time.Clock()
        
        # Stan systemu
        self.stability = 100
        self.is_running = True
        self.is_killed = False
        self.input_buffer = ""
        self.logs = ["[INFO] Kernel initialized.", "[INFO] System stability: 100%", "[HINT] Type 'help' for commands."]
        
        # Avatar
        self.avatar_pos = pygame.Vector2(400, 300)
        self.avatar_target = pygame.Vector2(400, 300)
        self.base_speed = 2.5
        self.current_speed = self.base_speed
        
        # Przeszkody i strefy
        self.obstacles = []  # List of pygame.Rect
        self.slow_zones = [] # List of pygame.Rect

    def add_log(self, text):
        self.logs.append(text)
        if len(self.logs) > 18: # Slightly fewer logs to keep space for input
            self.logs.pop(0)

    def handle_command(self, cmd):
        cmd = cmd.strip().lower()
        if not cmd: return

        if cmd == "help" or cmd == "sudo help":
            self.add_log("> Available: ls, status, clear, reboot")
            self.add_log("> Interference: inject_latency, spawn_deadlock, memory_leak, kill -9")
        elif cmd == "ls" or cmd == "ls /projects":
            self.add_log("> /projects: [hello_wasm]")
        elif cmd.startswith("cat "):
            filename = cmd.split(" ")[1]
            if filename == "hello_wasm":
                # Mock reading the file - in a real app, we might fetch it
                self.add_log("--- main.cpp ---")
                self.add_log("#include <iostream>")
                self.add_log("int main() {")
                self.add_log("  std::cout << 'Hello WASM!';")
                self.add_log("  return 0;")
                self.add_log("}")
            else:
                self.add_log(f"[ERROR] File not found: {filename}")
        elif cmd.startswith("run "):
            project = cmd.split(" ")[1]
            if project == "hello_wasm":
                self.add_log("[INFO] Launching hello_wasm.wasm...")
                self.add_log("[C++ MODULE] Simulation kernel starting...")
                self.add_log("[C++ MODULE] Memory check: PASSED.")
                # In a real implementation, we could call JS to load the WASM
            else:
                self.add_log(f"[ERROR] Project not found: {project}")
        elif cmd == "status":
            status = "STABLE" if self.stability > 70 else "DEGRADED" if self.stability > 30 else "CRITICAL"
            self.add_log(f"> SYSTEM_STATUS: {status} ({self.stability}%)")
            self.add_log(f"> PROCESS_ID: 0x{id(self)%10000:04X} | THREADS: 1")
        elif "latency" in cmd or "inject_latency" in cmd:
            self.stability = max(0, self.stability - 10)
            self.base_speed *= 0.8
            self.add_log("[WARNING] Latency injected. CPU cycles throttled.")
        elif "deadlock" in cmd or "spawn_deadlock" in cmd:
            new_rect = pygame.Rect(random.randint(50, 700), random.randint(300, 500), 60, 20)
            self.obstacles.append(new_rect)
            self.stability = max(0, self.stability - 15)
            self.add_log("[ERROR] Resource deadlock detected in Sector 7.")
        elif "leak" in cmd or "memory_leak" in cmd:
            new_rect = pygame.Rect(random.randint(50, 700), random.randint(300, 500), 100, 100)
            self.slow_zones.append(new_rect)
            self.stability = max(0, self.stability - 5)
            self.add_log("[WARNING] Memory leak detected. GC pressure increasing.")
        elif cmd == "kill -9":
            self.is_killed = True
            self.stability = 0
            self.add_log("[CRITICAL] Process killed by SIGKILL.")
        elif cmd == "clear":
            self.logs = []
        elif cmd == "reboot":
            self.stability = 100
            self.base_speed = 2.5
            self.is_killed = False
            self.obstacles = []
            self.slow_zones = []
            self.add_log("[INFO] System rebooted. All parameters nominal.")
        else:
            self.add_log(f"[ERROR] Unknown command: {cmd}")

    def draw_crt_effect(self):
        for y in range(0, 600, 4):
            pygame.draw.line(self.screen, (0, 20, 0), (0, y), (800, y))

    def draw_avatar(self):
        # Pulsing effect for the avatar
        import math
        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5
        
        avatar_color = COLOR_TEXT if not self.is_killed else (255, 0, 0)
        if self.stability < 40 and not self.is_killed:
            avatar_color = (200 + 55 * pulse, 100, 0) # Glitchy orange/red
            
        # Draw "ASCII" Avatar
        rect = (*self.avatar_pos, 24, 24)
        pygame.draw.rect(self.screen, avatar_color, rect, 1)
        
        # Internal "core"
        core_size = 4 + 4 * pulse
        pygame.draw.rect(self.screen, avatar_color, (self.avatar_pos.x + 12 - core_size/2, self.avatar_pos.y + 12 - core_size/2, core_size, core_size))

    async def main_loop(self):
        is_wasm = hasattr(sys, "getandroidapilevel") or "Emscripten" in sys.version or "pygbag" in sys.modules
        
        while self.is_running:
            # 1. External Events from JS Bridge
            if is_wasm:
                try:
                    import platform
                    js_event = platform.window.panic_event
                    if js_event:
                        # Handle specific events from JS buttons
                        if js_event == "latency": self.handle_command("inject_latency")
                        elif js_event == "deadlock": self.handle_command("spawn_deadlock")
                        elif js_event == "leak": self.handle_command("memory_leak")
                        elif js_event == "reboot": self.handle_command("reboot")
                        platform.window.panic_event = None
                except Exception:
                    pass

            # 2. Event handling
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

            # 3. Logic
            if not self.is_killed:
                # Update speed based on slow zones
                self.current_speed = self.base_speed
                for zone in self.slow_zones:
                    if zone.collidepoint(self.avatar_pos):
                        self.current_speed *= 0.3
                        break
                
                # Simple AI Movement
                if self.avatar_pos.distance_to(self.avatar_target) < 10:
                    self.avatar_target = pygame.Vector2(random.randint(50, 750), random.randint(300, 550))
                
                direction = (self.avatar_target - self.avatar_pos).normalize() if self.avatar_pos != self.avatar_target else pygame.Vector2(0,0)
                new_pos = self.avatar_pos + direction * self.current_speed
                
                # Collision with obstacles
                can_move = True
                temp_rect = pygame.Rect(new_pos.x, new_pos.y, 24, 24)
                for obs in self.obstacles:
                    if temp_rect.colliderect(obs):
                        can_move = False
                        self.avatar_target = pygame.Vector2(random.randint(50, 750), random.randint(300, 550))
                        break
                
                if can_move:
                    self.avatar_pos = new_pos

            # 4. Rendering
            self.screen.fill(COLOR_BG)
            
            # Draw Slow Zones (subtle dark green patches)
            for zone in self.slow_zones:
                pygame.draw.rect(self.screen, COLOR_SLOWZONE, zone)
                # Draw "dots" to make it look like "memory mud"
                for i in range(5):
                    px = zone.x + (pygame.time.get_ticks()//10 + i*20) % zone.width
                    py = zone.y + (i*15) % zone.height
                    pygame.draw.rect(self.screen, COLOR_TEXT, (px, py, 2, 2))
            
            # Draw Obstacles (Deadlocks)
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, COLOR_OBSTACLE, obs)
                pygame.draw.rect(self.screen, (255, 0, 0), obs, 1)

            # Draw Logs
            for i, log in enumerate(self.logs):
                text_surf = self.font.render(log, True, COLOR_TEXT)
                self.screen.blit(text_surf, (10, 10 + i * (FONT_SIZE + 2)))
            
            # Draw Input line
            input_text = f"admin@kernel:~$ {self.input_buffer}"
            if (pygame.time.get_ticks() // 500) % 2 == 0: input_text += "_"
            input_surf = self.font.render(input_text, True, COLOR_TEXT)
            self.screen.blit(input_surf, (10, 570))
            
            self.draw_avatar()
            self.draw_crt_effect()
            
            pygame.display.flip()
            self.clock.tick(60)
            await asyncio.sleep(0)

if __name__ == "__main__":
    terminal = TerminalAI()
    asyncio.run(terminal.main_loop())
