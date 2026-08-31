from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    DocumentItem,
    ChunkItem,
    CacheStats,
    ConfigUpdateRequest,
    HealthResponse
)
from app.rag.engine import rag_engine
from app.rag.indexer import corpus_index
from app.rag.cache import query_cache
from app.rag.llm import llm_service
from app.core.config import settings

router = APIRouter()

@router.post("/chat", response_model=QueryResponse, summary="Process RAG customer support query")
async def chat_query(request: QueryRequest):
    """
    Receives user query, retrieves relevant knowledge base chunks, evaluates in-scope
    vs out-of-scope confidence, and returns grounded answer or human escalation ticket.
    """
    if not request.query or len(request.query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters long.")
    
    try:
        response = rag_engine.process_query(request)
        return response
    except Exception as e:
        print(f"[!] Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal RAG Engine Error: {str(e)}")

@router.get("/documents", response_model=List[DocumentItem], summary="List official business documents")
async def list_documents():
    """Returns official business documents loaded into the knowledge base."""
    docs = corpus_index.get_documents_info()
    return [DocumentItem(**doc) for doc in docs]

@router.get("/chunks", response_model=List[ChunkItem], summary="Inspect overlapping chunks")
async def list_chunks(doc_name: Optional[str] = None):
    """Inspects all generated chunks with sliding-window overlap details."""
    all_chunks = corpus_index.get_all_chunks()
    if doc_name:
        all_chunks = [c for c in all_chunks if c["doc_name"] == doc_name]
    
    return [
        ChunkItem(
            chunk_id=c["chunk_id"],
            doc_name=c["doc_name"],
            title=c["doc_title"],
            section=c["section"],
            text=c["text"],
            char_start=c["char_start"],
            char_end=c["char_end"],
            token_approx=c["token_approx"]
        )
        for c in all_chunks
    ]

@router.post("/reload-corpus", summary="Reload and reindex document corpus")
async def reload_corpus():
    """Rescans data/documents directory and rebuilds BM25 + TF-IDF hybrid index."""
    try:
        corpus_index.build_index()
        query_cache.clear()
        return {
            "status": "success",
            "message": "Corpus successfully reloaded and reindexed",
            "documents_count": len(corpus_index.documents_info),
            "chunks_count": len(corpus_index.chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reindexing corpus: {str(e)}")

@router.get("/cache/stats", response_model=CacheStats, summary="Memory cache metrics")
async def get_cache_stats():
    """Returns in-memory cache hit/miss ratio and size."""
    return CacheStats(**query_cache.stats())

@router.post("/cache/clear", summary="Clear query cache")
async def clear_cache():
    """Empties in-memory cache."""
    query_cache.clear()
    return {"status": "success", "message": "Cache cleared successfully"}

@router.post("/config", summary="Update runtime configuration")
async def update_config(config: ConfigUpdateRequest):
    """Dynamically updates API Keys, similarity threshold, or model provider."""
    if config.gemini_api_key is not None:
        llm_service.gemini_key = config.gemini_api_key.strip()
        settings.GEMINI_API_KEY = config.gemini_api_key.strip()
    
    if config.confidence_threshold is not None:
        settings.SIMILARITY_THRESHOLD = config.confidence_threshold
        rag_engine.similarity_threshold = config.confidence_threshold
        
    if config.gemini_model is not None:
        llm_service.gemini_model = config.gemini_model.strip()
        settings.GEMINI_MODEL = config.gemini_model.strip()

    return {
        "status": "success",
        "message": "Configuration updated",
        "openai_configured": bool(llm_service.openai_key),
        "gemini_configured": bool(llm_service.gemini_key),
        "similarity_threshold": rag_engine.similarity_threshold
    }

@router.get("/health", response_model=HealthResponse, summary="System health status")
async def health_check():
    """Verifies operational status of RAG index, documents, and providers."""
    return HealthResponse(
        status="healthy" if corpus_index.is_indexed else "degraded",
        version=settings.VERSION,
        documents_indexed=len(corpus_index.documents_info),
        chunks_total=len(corpus_index.chunks),
        gemini_configured=bool(llm_service.gemini_key or llm_service.openai_key),
        cache_items=len(query_cache._cache),
        similarity_threshold=rag_engine.similarity_threshold
    )
