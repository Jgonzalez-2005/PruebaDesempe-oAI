from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router
from app.rag.indexer import corpus_index

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización al arrancar
    print(f"🚀 Iniciando {settings.PROJECT_NAME} v{settings.VERSION}...")
    if not corpus_index.is_indexed:
        corpus_index.build_index()
    yield
    # Limpieza al apagar
    print("🛑 Deteniendo servidor...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Sistema de Atención al Cliente Automatizada con RAG Determinista, Identidad Colombiana y Escalamiento a Soporte Humano para la Academia de Idiomas LinguaColombia.",
    lifespan=lifespan
)

# Configuración de CORS para permitir peticiones desde cualquier origen local (React/Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido al API de LinguaColombia AI Support",
        "docs_url": "/docs",
        "health_check": f"{settings.API_PREFIX}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
