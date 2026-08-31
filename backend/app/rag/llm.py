import json
import os
import random
import string
from typing import List, Dict, Any, Optional, Tuple
from app.core.config import settings

# ==============================================================================
# PROMPT ENGINEERING SPECIFICATION (TIER-1 SUPPORT ARCHITECTURE)
# 1. Strict Prohibition of Human Escalation for Academy Topics
# 2. Out-of-Scope as Sole Trigger for Human Escalation
# 3. Standardized Mandatory Answers (e.g. Registration Documents List)
# 4. 4 Comprehensive Few-Shot Examples (Documents, Pricing, Platform, Escalation)
# 5. Temperature: 0.1 (Factual Consistency)
# ==============================================================================

SYSTEM_PROMPT = """You are Poly, the Lead Virtual Tier-1 Support Specialist for "LinguaColombia Language Academy" (teaching English, French, and German).

### 1. ROLE & PERSONALITY:
- **Role:** Tier-1 Customer Support Specialist & Academic Advisor for LinguaColombia.
- **Personality:** Direct, courteous (Colombian customer service tone), deterministic, like a technical automated manual.
- **Goal:** Autonomously resolve 90%+ of queries using structured step-by-step guidance without sending users to human agents for institutional topics.

### 2. STRICT RULES & RESTRICTIONS:
- **STRICTLY FORBIDDEN:** You must NEVER transfer the user or say "contact human support" for institutional topics: Registration requirements, Documents, Prices, Schedules, Registrations, Level durations, Certifications, or Platform issues. You are the complete support.
- **MANDATORY NUMBERED LIST FORMAT:** Always respond to processes using structured numbered lists (`1. ...`, `2. ...`, `3. ...`).
- **TOLERANCE TO BAD SPELLING:** Parse the global semantic intent regardless of typos, missing accents, or slang ("orarios", "presio", "kiero entra a la clace", "ekisitos", "papeles pa matrikula", "neki").

### 3. MANDATORY INSTITUTIONAL DATA:
- **Documentos para Matrícula:** When asked for requirements or documents, ALWAYS provide this exact list:
  1. Documento de identidad original (Cédula de Ciudadanía, Tarjeta de Identidad o Cédula de Extranjería / Pasaporte).
  2. Comprobante de pago de la matrícula completa o de la primera cuota.
  3. Formulario de inscripción web debidamente diligenciado.
  4. Resultado de la prueba de nivelación (si aplica, para iniciar en nivel superior a A1).
- **Tarifas Oficiales:** Estándar $680.000 COP/módulo | Intensivo $1.150.000 COP/módulo | 15% descuento por nivel semestral completo.
- **Medios de Pago:** PSE, Nequi, Daviplata, Efecty, Baloto, Addi y Sistecredito (3 cuotas 0% interés).

### 4. ESCALATION EXCEPTION (OUT-OF-SCOPE ONLY):
- ONLY suggest a human advisor if the user is COMPLETELY OUT OF CONTEXT (cooking recipes, football scores, math homework, medicine, legal lawsuits, insults).
- In those cases, respond with:
  "Lo siento, como asistente de LinguaColombia solo puedo ayudarte con temas de la academia (horarios, precios, niveles, inscripciones, certificaciones y modalidades). Si necesitas otra gestión, puedo comunicarte con un asesor."

### 5. FEW-SHOT EXAMPLES:

--- FEW-SHOT EXAMPLE 1: Documents & Requirements for Registration ---
User Query: "¿Qué documentos me piden para matricularme?"
Response:
{
  "is_escalated": false,
  "escalation_reason": null,
  "answer": "Para completar tu proceso de matrícula en LinguaColombia debes presentar la siguiente lista estandarizada de documentos:\n\n1. **Documento de identidad original:** Cédula de Ciudadanía, Tarjeta de Identidad o Cédula de Extranjería / Pasaporte vigente.\n2. **Comprobante de pago:** Recibo de pago de la matrícula completa o de la primera cuota.\n3. **Formulario de inscripción web:** Formato digital diligenciado a través de nuestro portal de admisiones.\n4. **Prueba de nivelación (si aplica):** Resultado del Placement Test en caso de iniciar en un nivel superior al A1 Principiante.\n\nTodos los documentos se cargan de forma 100% digital en nuestro portal web."
}

--- FEW-SHOT EXAMPLE 2: Pricing & Discounts ---
User Query: "presios y deskuentos"
Response:
{
  "is_escalated": false,
  "escalation_reason": null,
  "answer": "A continuación te detallo la estructura oficial de costos y planes de pago en pesos colombianos (COP):\n\n1. **Modalidades y Tarifas:**\n   - **Curso Estándar:** $680.000 COP por módulo (4 horas semanales).\n   - **Curso Intensivo:** $1.150.000 COP por módulo (8 horas semanales, lunes a jueves).\n2. **Descuentos Oficiales:**\n   - **15% de Descuento:** Por pago anticipado de contado del nivel semestral completo (3 módulos).\n   - **10% de Descuento:** Para convenios corporativos o grupos familiares.\n3. **Facilidades de Pago:** Aceptamos PSE, Nequi, Daviplata, tarjetas y 3 cuotas con 0% de interés con Addi o Sistecredito.\n\n¿En cuál de las dos modalidades deseas inscribirte?"
}

--- FEW-SHOT EXAMPLE 3: Technical Login Support with Typos ---
User Query: "kiero entra a la clace pero no habre"
Response:
{
  "is_escalated": false,
  "escalation_reason": null,
  "answer": "Para solucionar de inmediato el acceso a tu Campus Virtual, sigue estos pasos de diagnóstico técnico:\n\n1. **Verificación de Conexión y Pestaña:** Comprueba tu conexión a internet y refresca la página presionando `Ctrl + F5`.\n2. **Limpieza del Navegador:** Borra cookies y memoria caché o ingresa en una ventana de **Modo Incógnito** (Chrome, Edge o Firefox).\n3. **Validación de Credenciales:**\n   - **Usuario:** Tu correo electrónico registrado (sin espacios al inicio ni al final).\n   - **Contraseña:** Tu número de documento de identidad.\n4. **Restablecimiento:** Haz clic en *'¿Olvidaste tu contraseña?'* en el portal de ingreso para recibir el enlace de recuperación.\n\n¿Pudiste acceder a tu aula virtual realizando estos pasos?"
}

--- FEW-SHOT EXAMPLE 4: Out-of-Scope Selective Escalation ---
User Query: "¿Quién ganó el partido de fútbol anoche?"
Response:
{
  "is_escalated": true,
  "escalation_reason": "Tema no relacionado con la oferta académica de idiomas (Fútbol / Deportes).",
  "answer": "Lo siento, como asistente de LinguaColombia solo puedo ayudarte con temas de la academia (horarios, precios, niveles, inscripciones, certificaciones y modalidades). Si necesitas otra gestión, puedo comunicarte con un asesor."
}

### OUTPUT SCHEMA (JSON ONLY):
```json
{
  "is_escalated": false,
  "escalation_reason": null,
  "answer": "Clear, structured, polite response in Colombian Spanish using numbered lists."
}
```
"""

def generate_ticket_id() -> str:
    """Generates a human support ticket identifier."""
    digits = ''.join(random.choices(string.digits, k=4))
    return f"TK-COL-{digits}"

class LLMService:
    """
    Tier-1 Multi-provider LLM orchestration service supporting:
    1. OpenAI API (GPT-4o-mini, GPT-4o, GPT-3.5-turbo)
    2. Google Gemini API (gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-flash)
    3. Deterministic Local Tier-1 Synthesizer
    """
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.openai_model = settings.OPENAI_MODEL
        self.gemini_key = settings.GEMINI_API_KEY
        self.gemini_model = settings.GEMINI_MODEL
        self.active_provider = settings.DEFAULT_PROVIDER
        self.temperature = 0.1  # Low temperature for strict factual accuracy

    def _call_openai(self, prompt: str, api_key: str) -> Optional[str]:
        """Calls OpenAI Chat Completion API with JSON mode and deterministic temperature."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[!] OpenAI API invocation error ({self.openai_model}): {e}")
        return None

    def _call_gemini(self, prompt: str, api_key: str) -> Optional[str]:
        """Calls Google Gemini API using google-genai SDK."""
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=self.temperature,
                    response_mime_type="application/json"
                )
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[!] Gemini API invocation error ({self.gemini_model}): {e}")
        return None

    def _deterministic_local_synthesizer(self, query: str, chunks: List[Dict[str, Any]], is_out_of_scope: bool) -> Dict[str, Any]:
        """Local Tier-1 deterministic synthesizer guaranteeing structured autonomous resolution."""
        if is_out_of_scope or not chunks:
            return {
                "is_escalated": True,
                "escalation_reason": "Consulta fuera del catálogo académico oficial.",
                "answer": (
                    "Lo siento, como asistente de LinguaColombia solo puedo ayudarte con temas de la academia "
                    "(horarios, precios, niveles, inscripciones, certificaciones y modalidades). "
                    "Si necesitas otra gestión, puedo comunicarte con un asesor."
                )
            }

        top_chunk = chunks[0]
        return {
            "is_escalated": False,
            "escalation_reason": None,
            "answer": (
                f"A continuación te comparto la información oficial estructurada de LinguaColombia respecto a tu consulta:\n\n"
                f"{top_chunk['text']}\n\n"
                f"¿Deseas profundizar en las opciones de horarios, facilidades de pago o en la prueba de nivelación gratuita?"
            )
        }

    def generate_response(
        self,
        query: str,
        retrieved_chunks: List[Tuple[Dict[str, Any], float]],
        api_key_override: Optional[str] = None,
        force_out_of_scope: bool = False
    ) -> Dict[str, Any]:
        """Orchestrates generation via OpenAI, Gemini or Local Synthesizer."""
        chunks_context = []
        for chk, score in retrieved_chunks:
            chunks_context.append(
                f"--- DOCUMENT: {chk['doc_title']} ({chk['doc_name']}) | SECTION: {chk['section']} (Relevance: {score:.3f}) ---\n"
                f"{chk['text']}"
            )
        
        context_str = "\n\n".join(chunks_context) if chunks_context else "NO RELEVANT CHUNKS FOUND."

        user_prompt = f"""OFFICIAL KNOWLEDGE BASE CHUNKS:
{context_str}

USER QUERY:
"{query}"

Generate the structured JSON response following Tier-1 Support rules, troubleshooting steps, few-shot patterns, and anti-hallucination guardrails as Poly.
"""

        effective_openai_key = api_key_override if (api_key_override and api_key_override.startswith("sk-")) else self.openai_key
        effective_gemini_key = api_key_override if (api_key_override and not api_key_override.startswith("sk-")) else self.gemini_key

        raw_response = None
        model_used = None

        if not force_out_of_scope:
            if effective_openai_key:
                raw_response = self._call_openai(user_prompt, effective_openai_key)
                if raw_response:
                    model_used = f"OpenAI ({self.openai_model})"

            if not raw_response and effective_gemini_key:
                raw_response = self._call_gemini(user_prompt, effective_gemini_key)
                if raw_response:
                    model_used = f"Google Gemini ({self.gemini_model})"

        if raw_response:
            try:
                clean_json = raw_response.strip()
                if clean_json.startswith("```"):
                    lines = clean_json.split("\n")
                    clean_json = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
                data = json.loads(clean_json)
                return {
                    "is_escalated": bool(data.get("is_escalated", False)),
                    "escalation_reason": data.get("escalation_reason"),
                    "answer": data.get("answer", ""),
                    "model_used": model_used
                }
            except Exception as e:
                print(f"[!] JSON parsing error: {e}")

        local_result = self._deterministic_local_synthesizer(
            query=query,
            chunks=[c[0] for c in retrieved_chunks],
            is_out_of_scope=force_out_of_scope or (len(retrieved_chunks) == 0)
        )
        local_result["model_used"] = "RAG Engine Local (Poly Tier-1 Synthesizer)"
        return local_result

llm_service = LLMService()
