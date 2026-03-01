from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI(title="AI Terminal Portfolio - Admin Console")

# Montujemy pliki statyczne oraz wygenerowany terminal
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/build", StaticFiles(directory="engine/build/web"), name="build")

@app.get("/terminal")
async def get_terminal():
    """Serwuje wygenerowany przez pygbag interfejs terminala."""
    return FileResponse("engine/build/web/index.html")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>KERNEL ACCESS: Portfolio AI</title>
        <style>
            body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; margin: 0; display: flex; height: 100vh; overflow: hidden; }
            #sidebar { width: 300px; border-right: 2px solid #00ff41; padding: 20px; box-shadow: 5px 0 15px rgba(0, 255, 65, 0.2); z-index: 10; }
            #main-terminal { flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #000; position: relative; }
            .btn-panic { background: #1a0000; color: #ff0000; border: 1px solid #ff0000; padding: 10px; width: 100%; margin-bottom: 10px; cursor: pointer; font-weight: bold; }
            .btn-panic:hover { background: #ff0000; color: #000; }
            .status-panel { margin-top: 20px; font-size: 0.8em; border: 1px solid #00ff41; padding: 10px; }
            iframe { border: none; width: 800px; height: 600px; box-shadow: 0 0 20px rgba(0, 255, 65, 0.3); }
            h2 { font-size: 1.2em; text-transform: uppercase; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <div id="sidebar">
            <h2>Interference Tools</h2>
            <p>Select action to disrupt AI Kernel stability:</p>
            
            <button class="btn-panic" onclick="triggerPanic('latency')">INJECT LATENCY</button>
            <button class="btn-panic" onclick="triggerPanic('deadlock')">SPAWN DEADLOCK</button>
            <button class="btn-panic" onclick="triggerPanic('leak')">MEMORY LEAK</button>
            <button class="btn-panic" style="background: #440000; color: #ff0000; border-color: #ff0000;" onclick="triggerPanic('kill')">KILL -9</button>
            <button class="btn-panic" style="background: #222; color: #00ff41; border-color: #00ff41;" onclick="triggerPanic('reboot')">REBOOT KERNEL</button>

            <div class="status-panel">
                <strong>[SYSTEM STATUS]</strong><br>
                Uptime: 1024s<br>
                Load: 0.45<br>
                Security: BREACHED
            </div>
        </div>
        
        <div id="main-terminal">
            <div style="margin-bottom: 10px; font-size: 0.9em;">> KERNEL_STREAM_ID: 0x88AF2</div>
            <iframe id="terminal-frame" src="/terminal"></iframe>
            <div style="margin-top: 10px; font-size: 0.7em;">Press CTRL+C to terminate session.</div>
        </div>

        <script>
            function triggerPanic(type) {
                console.log("Kernel Panic Triggered: " + type);
                const iframe = document.getElementById('terminal-frame');
                // Przekazujemy zdarzenie do iframe
                if (iframe.contentWindow) {
                    iframe.contentWindow.panic_event = type;
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
