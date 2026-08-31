import time
import threading
from typing import Dict, Any, Optional
from app.core.config import settings
from app.rag.indexer import normalize_text

class QueryCache:
    """
    Caché en memoria RAM (LRU/TTL) para responder de forma instantánea (<2ms)
    a consultas frecuentes o repetidas, reduciendo la latencia y los costos de API.
    """
    def __init__(self, max_items: int = settings.CACHE_MAX_ITEMS, ttl_seconds: int = settings.CACHE_TTL_SECONDS):
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def _normalize_key(self, query: str) -> str:
        """Normaliza la consulta para un cache lookup uniforme."""
        return normalize_text(query.strip())

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        """Recupera un resultado en caché si aún no ha expirado."""
        if not settings.CACHE_ENABLED:
            return None

        key = self._normalize_key(query)
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() - entry["timestamp"] < self.ttl_seconds:
                    self.hits += 1
                    # Actualizar acceso para LRU
                    entry["last_accessed"] = time.time()
                    return entry["data"]
                else:
                    # Expirado
                    del self._cache[key]

            self.misses += 1
            return None

    def set(self, query: str, data: Dict[str, Any]):
        """Guarda un resultado en caché."""
        if not settings.CACHE_ENABLED:
            return

        key = self._normalize_key(query)
        with self._lock:
            # Control de tamaño máximo (LRU simple)
            if len(self._cache) >= self.max_items and key not in self._cache:
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]["last_accessed"])
                del self._cache[oldest_key]

            self._cache[key] = {
                "data": data,
                "timestamp": time.time(),
                "last_accessed": time.time()
            }

    def clear(self):
        """Limpia la caché."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0

    def stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de la caché."""
        with self._lock:
            total_requests = self.hits + self.misses
            ratio = (self.hits / total_requests) if total_requests > 0 else 0.0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "size": len(self._cache),
                "max_size": self.max_items,
                "hit_ratio": round(ratio, 3)
            }

# Instancia global
query_cache = QueryCache()
