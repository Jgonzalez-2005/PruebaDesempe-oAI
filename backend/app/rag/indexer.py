import os
import re
import unicodedata
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.rag.chunker import DocumentChunker
from app.core.config import settings

# Stopwords comunes en español para no diluir el cálculo de similitud
SPANISH_STOPWORDS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una",
    "su", "al", "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "este", "si", "porque", "esta", "entre",
    "cuando", "muy", "sin", "sobre", "tambien", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos",
    "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mi",
    "antes", "algunos", "que", "unos", "yo", "otro", "otras", "otra", "el", "tanto", "esa", "estos", "mucho",
    "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi",
    "mis", "tus", "ellas", "nosotras", "vosotros", "vosotras", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya",
    "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras",
    "esos", "esas", "estoy", "estas", "esta", "estamos", "estais", "estan", "este", "estes", "estemos", "esteis",
    "esten", "estare", "estaras", "estara", "estaremos", "estareis", "estaran", "estaria", "estarias", "estariamos",
    "estariais", "estarian", "estaba", "estabas", "estabamos", "estabais", "estaban", "estuve", "estuviste", "estuvo",
    "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuvieramos", "estuvierais", "estuvieran",
    "estuviese", "estuvieses", "estuviesemos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados",
    "estadas", "estad", "he", "has", "ha", "hemos", "habeis", "han", "haya", "hayas", "hayamos", "hayais", "hayan",
    "habre", "habras", "habra", "habremos", "habreis", "habran", "habria", "habrias", "habriamos", "habriais", "habrian",
    "habia", "habias", "habiamos", "habiais", "habian", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron",
    "hubiera", "hubieras", "hubieramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubiesemos", "hubieseis",
    "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son",
    "sea", "seas", "seamos", "seais", "sean", "sere", "seras", "sera", "seremos", "sereis", "seran", "seria",
    "serias", "seriamos", "seriais", "serian", "era", "eras", "eramos", "erais", "eran", "fui", "fuiste", "fue",
    "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fueramos", "fuerais", "fueran", "fuese", "fueses", "fuesemos",
    "fueseis", "fuesen", "siendo", "sido", "tengo", "tienes", "tiene", "tenemos", "teneis", "tienen", "tenga", "tengas"
}

def normalize_text(text: str) -> str:
    """Normaliza texto eliminando tildes y caracteres especiales."""
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())

def tokenize_for_bm25(text: str) -> List[str]:
    """Tokeniza y filtra palabras vacías para BM25."""
    norm = normalize_text(text)
    tokens = [w for w in norm.split() if len(w) > 1 and w not in SPANISH_STOPWORDS]
    return tokens if tokens else norm.split()

class InMemoryCorpusIndex:
    """
    Índice híbrido en memoria RAM que combina BM25 (relevancia léxica precisa)
    y TF-IDF con n-gramas (similitud semántica de frases y sub-palabras).
    """
    def __init__(self, docs_dir: Path = settings.DOCS_DIR):
        self.docs_dir = Path(docs_dir)
        self.chunker = DocumentChunker(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.chunks: List[Dict[str, Any]] = []
        self.documents_info: List[Dict[str, Any]] = []
        self.vectorizer: TfidfVectorizer = None
        self.chunk_vectors = None
        self.bm25: BM25Okapi = None
        self.tokenized_corpus: List[List[str]] = []
        self.is_indexed: bool = False
        
        self.build_index()

    def build_index(self):
        """Lee todos los documentos y construye el índice híbrido BM25 + TF-IDF."""
        self.chunks = []
        self.documents_info = []
        self.tokenized_corpus = []
        
        if not self.docs_dir.exists():
            self.docs_dir.mkdir(parents=True, exist_ok=True)
            return

        doc_files = sorted(list(self.docs_dir.glob("*.html")) + list(self.docs_dir.glob("*.txt")) + list(self.docs_dir.glob("*.md")))
        
        corpus_texts = []
        for file_path in doc_files:
            file_size = file_path.stat().st_size
            file_chunks = self.chunker.process_file(file_path)
            
            sections = list({chk["section"] for chk in file_chunks})
            doc_title = file_chunks[0]["doc_title"] if file_chunks else file_path.name
            
            self.documents_info.append({
                "filename": file_path.name,
                "title": doc_title,
                "size_bytes": file_size,
                "chunk_count": len(file_chunks),
                "sections": sections
            })
            
            for chk in file_chunks:
                self.chunks.append(chk)
                # Enriquecer texto indexable con título y sección repetidos estratégicamente
                searchable_text = f"{chk['doc_title']} {chk['section']} {chk['text']}"
                norm_text = normalize_text(searchable_text)
                corpus_texts.append(norm_text)
                
                # Tokenizar para BM25
                tokens = tokenize_for_bm25(searchable_text)
                self.tokenized_corpus.append(tokens)

        if corpus_texts and self.tokenized_corpus:
            # 1. TF-IDF con palabras clave
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                sublinear_tf=True,
                stop_words=list(SPANISH_STOPWORDS)
            )
            self.chunk_vectors = self.vectorizer.fit_transform(corpus_texts)
            
            # 2. BM25
            self.bm25 = BM25Okapi(self.tokenized_corpus)
            
            self.is_indexed = True
            print(f"[✓] Índice RAG Híbrido (BM25 + TF-IDF) construido: {len(doc_files)} documentos, {len(self.chunks)} chunks.")
        else:
            self.is_indexed = False
            print("[!] Advertencia: No se encontraron documentos para indexar.")

    def search(self, query: str, top_k: int = settings.TOP_K_CHUNKS) -> List[Tuple[Dict[str, Any], float]]:
        """
        Búsqueda híbrida que combina BM25 y Similitud Coseno TF-IDF.
        Retorna los fragmentos ordenados por score normalizado (0.0 a 1.0).
        """
        if not self.is_indexed or not self.chunks or self.vectorizer is None or self.bm25 is None:
            return []

        norm_query = normalize_text(query)
        query_tokens = tokenize_for_bm25(query)
        
        # 1. Puntuación BM25
        bm25_scores = np.array(self.bm25.get_scores(query_tokens)) if query_tokens else np.zeros(len(self.chunks))
        raw_bm25_max = float(np.max(bm25_scores)) if len(bm25_scores) > 0 else 0.0
        
        # Si no hubo ninguna coincidencia léxica en BM25
        if raw_bm25_max <= 0.0:
            norm_bm25 = np.zeros(len(self.chunks))
        else:
            norm_bm25 = bm25_scores / raw_bm25_max

        # 2. Puntuación TF-IDF Cosine Similarity
        query_vec = self.vectorizer.transform([norm_query])
        tfidf_similarities = cosine_similarity(query_vec, self.chunk_vectors)[0]
        
        # 3. Puntuación Híbrida Ponderada
        # Si BM25 es 0 y TF-IDF es casi 0, el score resultante será ~0.0
        if raw_bm25_max <= 0.0:
            hybrid_scores = tfidf_similarities
        else:
            hybrid_scores = (0.60 * norm_bm25) + (0.40 * tfidf_similarities)
        
        # Si la consulta contiene keywords muy específicas de la base, reflejarlo en el score
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(hybrid_scores[idx])
            results.append((self.chunks[idx], score))
            
        return results

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        return self.chunks

    def get_documents_info(self) -> List[Dict[str, Any]]:
        return self.documents_info

# Instancia global del índice
corpus_index = InMemoryCorpusIndex()
