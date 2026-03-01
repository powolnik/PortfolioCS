from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
import os

app = FastAPI(title="AI Terminal Portfolio")

# Montujemy pliki silnika bezpośrednio w głównym katalogu (dla Pygbag)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/pkg", StaticFiles(directory="static/pkg"), name="pkg")

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

app.mount("/", StaticFiles(directory="engine/build/web", html=True), name="engine")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
