import time
import re
from typing import Dict, Any, Optional, List, Tuple
from app.core.config import settings
from app.rag.indexer import corpus_index
from app.rag.cache import query_cache
from app.rag.llm import llm_service, generate_ticket_id
from app.rag.conversational import check_conversational_intent
from app.models.schemas import QueryRequest, QueryResponse, Citation

OUT_OF_SCOPE_KEYWORDS = [
    # Temas 100% ajenos a la academia de idiomas
    "cocina", "reposteria", "culinaria", "chef", "gastronomia", "receta", "recetas",
    "futbol", "partido", "gol", "champions", "liga",
    "matematicas", "calculo", "algebra", "tarea de matematicas",
    "arriendo", "arrendar", "alquiler de salon", "alquilar salon", "evento", "fiesta",
    "medicina", "enfermeria", "medico", "odontologia", "cita medica", "salud",
    "manejo", "conducir", "licencia de conduccion", "pase de moto", "carro",
    "baile", "danza", "salsa", "bachata",
    "programacion", "python", "javascript", "desarrollo web", "software",
    "abogado", "juridico", "demanda", "tutela", "contrato legal"
]

class RAGEngine:
    """
    Core Python RAG Engine orchestrating conversational intent detection,
    in-memory hybrid search, out-of-scope evaluation, human escalation triggers,
    LLM generation, and caching.
    """
    def __init__(self):
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD

    def is_explicitly_out_of_scope(self, query: str) -> Tuple[bool, Optional[str]]:
        """Detects explicitly off-topic requests alien to the language academy."""
        query_lower = query.lower()
        for kw in OUT_OF_SCOPE_KEYWORDS:
            if re.search(rf"\b{re.escape(kw)}\b", query_lower):
                return True, f"Tema no relacionado con la oferta académica de idiomas ({kw.capitalize()})"
        return False, None

    def process_query(self, request: QueryRequest) -> QueryResponse:
        start_time = time.perf_counter()
        
        # 1. In-Memory Cache Lookup for sub-millisecond repeat queries
        if request.use_cache:
            cached_data = query_cache.get(request.query)
            if cached_data:
                latency = round((time.perf_counter() - start_time) * 1000, 2)
                return QueryResponse(
                    query=request.query,
                    answer=cached_data["answer"],
                    is_escalated=cached_data["is_escalated"],
                    escalation_reason=cached_data.get("escalation_reason"),
                    ticket_id=cached_data.get("ticket_id"),
                    confidence_score=cached_data["confidence_score"],
                    citations=[Citation(**c) for c in cached_data.get("citations", [])],
                    latency_ms=latency,
                    from_cache=True,
                    model_used=cached_data.get("model_used", "Cache Hit")
                )

        # 2. Check for explicit Out-of-Scope first
        is_keyword_oos, oos_reason = self.is_explicitly_out_of_scope(request.query)

        # 3. Conversational Intent & FAQ Handler (If not explicitly off-topic)
        if not is_keyword_oos:
            conversational_match = check_conversational_intent(request.query)
            if conversational_match:
                latency = round((time.perf_counter() - start_time) * 1000, 2)
                response_data = {
                    "query": request.query,
                    "answer": conversational_match["answer"],
                    "is_escalated": False,
                    "escalation_reason": None,
                    "ticket_id": None,
                    "confidence_score": 1.0,
                    "citations": [],
                    "latency_ms": latency,
                    "from_cache": False,
                    "model_used": conversational_match["model_used"]
                }
                if request.use_cache:
                    query_cache.set(request.query, response_data)
                
                return QueryResponse(
                    query=response_data["query"],
                    answer=response_data["answer"],
                    is_escalated=False,
                    escalation_reason=None,
                    ticket_id=None,
                    confidence_score=1.0,
                    citations=[],
                    latency_ms=latency,
                    from_cache=False,
                    model_used=response_data["model_used"]
                )

        # 4. Hybrid Retrieval (BM25 + TF-IDF in memory)
        retrieved_results = corpus_index.search(request.query, top_k=settings.TOP_K_CHUNKS)
        max_score = retrieved_results[0][1] if retrieved_results else 0.0
        
        # 5. Out-of-Scope & Confidence Guardrails
        is_low_confidence = (max_score < self.similarity_threshold)
        force_out_of_scope = is_keyword_oos or is_low_confidence
        escalation_reason = oos_reason or ("Similitud insuficiente con documentos oficiales (< {:.2f})".format(self.similarity_threshold) if is_low_confidence else None)

        # 6. Filter citations
        citations: List[Citation] = []
        if is_keyword_oos:
            max_score = 0.0
        else:
            for chk, score in retrieved_results:
                if score >= 0.05:
                    citations.append(Citation(
                        doc_id=chk["doc_name"],
                        doc_title=chk["doc_title"],
                        section=chk["section"],
                        snippet=chk["text"][:280] + ("..." if len(chk["text"]) > 280 else ""),
                        score=round(score, 3),
                        chunk_id=chk["chunk_id"]
                    ))

        # 7. LLM Synthesis or Grounded Fallback
        llm_result = llm_service.generate_response(
            query=request.query,
            retrieved_chunks=retrieved_results,
            api_key_override=request.api_key,
            force_out_of_scope=force_out_of_scope
        )

        is_escalated = llm_result.get("is_escalated", False) or force_out_of_scope
        final_reason = llm_result.get("escalation_reason") or escalation_reason if is_escalated else None
        ticket_id = generate_ticket_id() if is_escalated else None
        
        latency = round((time.perf_counter() - start_time) * 1000, 2)

        response_data = {
            "query": request.query,
            "answer": llm_result.get("answer", ""),
            "is_escalated": is_escalated,
            "escalation_reason": final_reason,
            "ticket_id": ticket_id,
            "confidence_score": round(max_score, 3),
            "citations": [c.model_dump() for c in citations],
            "latency_ms": latency,
            "from_cache": False,
            "model_used": llm_result.get("model_used", "Engine")
        }

        # 8. Save in Cache
        if request.use_cache:
            query_cache.set(request.query, response_data)

        return QueryResponse(
            query=response_data["query"],
            answer=response_data["answer"],
            is_escalated=response_data["is_escalated"],
            escalation_reason=response_data["escalation_reason"],
            ticket_id=response_data["ticket_id"],
            confidence_score=response_data["confidence_score"],
            citations=citations,
            latency_ms=latency,
            from_cache=False,
            model_used=response_data["model_used"]
        )

rag_engine = RAGEngine()
