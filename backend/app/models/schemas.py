from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., description="Pregunta del usuario en lenguaje natural", min_length=2)
    api_key: Optional[str] = Field(None, description="Clave API de Gemini opcional para sobrescribir la del sistema")
    use_cache: bool = Field(True, description="Si es True, aprovecha la caché en memoria para respuestas ultra rápidas")

class Citation(BaseModel):
    doc_id: str = Field(..., description="Nombre del archivo fuente")
    doc_title: str = Field(..., description="Título legible del documento")
    section: str = Field(..., description="Sección o encabezado de origen")
    snippet: str = Field(..., description="Fragmento de texto extraído")
    score: float = Field(..., description="Puntaje de similitud / relevancia (0.0 a 1.0)")
    chunk_id: str = Field(..., description="Identificador único del chunk")

class QueryResponse(BaseModel):
    query: str
    answer: str
    is_escalated: bool = Field(..., description="Indica si la consulta fue escalada a un asesor humano")
    escalation_reason: Optional[str] = Field(None, description="Motivo por el cual fue escalada")
    ticket_id: Optional[str] = Field(None, description="Código de ticket generado para el caso humano")
    confidence_score: float = Field(..., description="Nivel de confianza o similitud más alto encontrado")
    citations: List[Citation] = Field(default_factory=list, description="Citas y evidencias documentales")
    latency_ms: float = Field(..., description="Tiempo total de procesamiento en milisegundos")
    from_cache: bool = Field(False, description="Indica si la respuesta provino de la caché en memoria")
    model_used: str = Field(..., description="Modelo o motor utilizado para generar la respuesta")

class DocumentItem(BaseModel):
    filename: str
    title: str
    size_bytes: int
    chunk_count: int
    sections: List[str]

class ChunkItem(BaseModel):
    chunk_id: str
    doc_name: str
    title: str
    section: str
    text: str
    char_start: int
    char_end: int
    token_approx: int

class CacheStats(BaseModel):
    hits: int
    misses: int
    size: int
    max_size: int
    hit_ratio: float

class ConfigUpdateRequest(BaseModel):
    gemini_api_key: Optional[str] = None
    confidence_threshold: Optional[float] = None
    gemini_model: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    documents_indexed: int
    chunks_total: int
    gemini_configured: bool
    cache_items: int
    similarity_threshold: float
