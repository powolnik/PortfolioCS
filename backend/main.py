from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
import os

app = FastAPI(title="AI Terminal Portfolio")

# Montujemy pliki statyczne
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/engine", StaticFiles(directory="engine/build/web"), name="engine")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Służymy wersję Pygbag jako główną stronę
    index_path = "engine/build/web/index.html"
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    return HTMLResponse("<h1>Engine not built</h1><p>Run 'pygbag engine' to build.</p>")

@app.get("/source/{project_name}")
async def get_source(project_name: str):
    # Mapowanie nazw na ścieżki (bezpieczeństwo: sprawdzamy czy plik istnieje)
    paths = {
        "hello_wasm": "projects_cpp/hello_wasm/main.cpp"
    }
    
    file_path = paths.get(project_name)
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return PlainTextResponse(f.read())
    return PlainTextResponse("Error: Source not found.", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
