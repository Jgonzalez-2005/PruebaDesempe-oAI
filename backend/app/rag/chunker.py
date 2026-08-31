import re
from typing import List, Dict, Any
from pathlib import Path
from html.parser import HTMLParser

class DocumentChunker:
    """
    Procesador de documentos con chunking semántico y solapamiento (overlap)
    para preservar el contexto entre secciones.
    """
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean_html(self, html_content: str) -> str:
        """Convierte HTML a texto plano estructurado conservando saltos de línea."""
        # Reemplazar encabezados y párrafos con saltos de línea
        text = re.sub(r'<(h[1-6]|p|li|header|section|div)[^>]*>', '\n', html_content, flags=re.IGNORECASE)
        # Quitar todas las demás etiquetas HTML
        text = re.sub(r'<[^>]+>', ' ', text)
        # Normalizar espacios
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)

    def extract_sections_from_html(self, html_content: str, filename: str) -> List[Dict[str, Any]]:
        """
        Extrae secciones delimitadas por etiquetas <section> o <h2> con su título y contenido.
        """
        # Extraer título del documento
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        doc_title = title_match.group(1).strip() if title_match else filename

        sections = []
        # Buscar todas las secciones
        section_pattern = re.compile(r'<section\s+id=[\'"]([^\'"]*)[\'"][^>]*>(.*?)</section>', re.IGNORECASE | re.DOTALL)
        matches = list(section_pattern.finditer(html_content))

        if matches:
            for match in matches:
                sec_id = match.group(1)
                sec_content = match.group(2)
                
                # Extraer título h2 o h3
                h2_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', sec_content, re.IGNORECASE | re.DOTALL)
                sec_title = h2_match.group(1).strip() if h2_match else sec_id.replace('-', ' ').title()
                
                plain_text = self.clean_html(sec_content)
                sections.append({
                    "doc_name": filename,
                    "doc_title": doc_title,
                    "section_id": sec_id,
                    "section_title": sec_title,
                    "text": plain_text
                })
        else:
            # Fallback para archivos sin <section>
            plain_text = self.clean_html(html_content)
            sections.append({
                "doc_name": filename,
                "doc_title": doc_title,
                "section_id": "main",
                "section_title": "Contenido General",
                "text": plain_text
            })

        return sections

    def create_overlapping_chunks(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplica ventana deslizante con solapamiento (overlap) sobre cada sección de texto.
        """
        chunks = []
        chunk_counter = 1

        for sec in sections:
            text = sec["text"]
            text_len = len(text)
            
            if text_len <= self.chunk_size:
                chunks.append({
                    "chunk_id": f"{sec['doc_name']}_chk_{chunk_counter:03d}",
                    "doc_name": sec["doc_name"],
                    "doc_title": sec["doc_title"],
                    "section": sec["section_title"],
                    "text": text,
                    "char_start": 0,
                    "char_end": text_len,
                    "token_approx": len(text.split())
                })
                chunk_counter += 1
                continue

            start = 0
            while start < text_len:
                end = min(start + self.chunk_size, text_len)
                
                # Intentar cortar en el límite de una palabra o frase para no romper términos
                if end < text_len:
                    last_newline = text.rfind('\n', start, end)
                    last_period = text.rfind('. ', start, end)
                    last_space = text.rfind(' ', start, end)
                    
                    if last_newline != -1 and last_newline > start + (self.chunk_size // 2):
                        end = last_newline + 1
                    elif last_period != -1 and last_period > start + (self.chunk_size // 2):
                        end = last_period + 2
                    elif last_space != -1 and last_space > start + (self.chunk_size // 2):
                        end = last_space + 1

                chunk_text = text[start:end].strip()
                
                if len(chunk_text) > 30: # Evitar fragmentos residuales insignificantes
                    chunks.append({
                        "chunk_id": f"{sec['doc_name']}_chk_{chunk_counter:03d}",
                        "doc_name": sec["doc_name"],
                        "doc_title": sec["doc_title"],
                        "section": sec["section_title"],
                        "text": chunk_text,
                        "char_start": start,
                        "char_end": end,
                        "token_approx": len(chunk_text.split())
                    })
                    chunk_counter += 1

                if end >= text_len:
                    break

                # Desplazar inicio aplicando el solapamiento
                start = end - self.chunk_overlap
                if start < 0 or start >= end:
                    start = end

        return chunks

    def process_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Lee un archivo y retorna todos sus chunks con metadata y solapamiento."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = self.extract_sections_from_html(content, file_path.name)
        return self.create_overlapping_chunks(sections)
