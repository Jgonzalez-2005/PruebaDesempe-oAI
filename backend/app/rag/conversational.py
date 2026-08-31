import re
import unicodedata
from typing import Optional, Dict, Any, List

# Diccionario exhaustivo de normalización fonética y corrección de jerga de chat
TYPO_DICTIONARY = {
    # Saludos
    "ola": "hola",
    "hla": "hola",
    "hol": "hola",
    "olaa": "hola",
    "olaaa": "hola",
    "holaa": "hola",
    "holaaa": "hola",
    "holas": "hola",
    "holis": "hola",
    "wena": "buenas",
    "wenas": "buenas",
    "bunas": "buenas",
    "buenass": "buenas",
    "q hubo": "hola",
    "quiubo": "hola",
    "q mas": "hola",
    "que mas": "hola",
    "q tal": "hola",
    "bns dias": "buenos dias",
    "bns tardes": "buenas tardes",
    "bns noches": "buenas noches",
    
    # Documentos y requisitos
    "dokumentos": "documentos",
    "dokumento": "documento",
    "ekisitos": "requisitos",
    "rekisitos": "requisitos",
    "recisitos": "requisitos",
    "requicitos": "requisitos",
    "papeleo": "documentos",
    "papeles": "documentos",
    "papel": "documento",
    "cedula": "documento de identidad",
    
    # Intenciones técnicas y acceso
    "kiero": "quiero",
    "qiero": "quiero",
    "entra": "entrar",
    "ingreza": "ingresar",
    "ingresa": "ingresar",
    "ingrezar": "ingresar",
    "clace": "clase",
    "clasis": "clases",
    "klases": "clases",
    "klase": "clase",
    "sirbe": "sirve",
    "no sirbe": "no sirve",
    "no habre": "no abre",
    "caida": "caida",
    "pegada": "bloqueada",
    "traba": "bloquea",
    "trabada": "bloqueada",
    "clave": "clave",
    "contra": "contrasena",
    "contrasenia": "contrasena",
    "pasword": "contrasena",
    "password": "contrasena",
    
    # Precios y pagos
    "kuesta": "cuesta",
    "kuanto": "cuanto",
    "bale": "vale",
    "presio": "precio",
    "presios": "precios",
    "presyo": "precio",
    "deskuento": "descuento",
    "deskuentos": "descuentos",
    "promosion": "promocion",
    "promosiones": "promociones",
    "kostos": "costos",
    "neki": "nequi",
    "dabiplata": "daviplata",
    "pze": "pse",
    "adi": "addi",
    "sistekredito": "sistecredito",
    "efecti": "efecty",
    "efekty": "efecty",
    "targeta": "tarjeta",
    "tarxeta": "tarjeta",
    
    # Idiomas y cursos
    "ingle": "ingles",
    "ingls": "ingles",
    "franses": "frances",
    "alemn": "aleman",
    "kurso": "curso",
    "kursos": "cursos",
    "curzo": "curso",
    "durasion": "duracion",
    "escribirme": "inscribirme",
    "inscribir": "inscribirme",
    "inscribirme": "inscribirme",
    "matrikula": "matricula",
    "matrikulas": "matriculas",
    "matricularm": "matricularme",
    
    # Horarios
    "orario": "horario",
    "orarios": "horarios",
    "savado": "sabado",
    "savados": "sabados",
    "savatino": "sabatino",
    "savatinos": "sabatinos",
    
    # Exámenes y clasificaciones
    "clasifikasion": "clasificacion",
    "nivelasion": "nivelacion",
    "plasement": "placement",
    "tofel": "toefl",
    "esamen": "examen",
    "ekzamen": "examen",
    
    # Agradecimientos y despedidas
    "grax": "gracias",
    "grasias": "gracias",
    "graciass": "gracias",
    "grasiass": "gracias",
    "thx": "gracias",
    "ty": "gracias",
    "xao": "chao",
    "chaoo": "chao",
    "bai": "chao",
    "bye": "chao"
}

def clean_and_normalize(text: str) -> str:
    """
    Normaliza el texto eliminando tildes, reduciendo caracteres repetidos (ej. 'hooooola' -> 'hola')
    y estandarizando términos mal escritos para análisis semántico estricto de Nivel 1.
    """
    if not text:
        return ""
    
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    
    # Reducir caracteres repetidos consecutivos (ej. 'olaaaa' -> 'ola')
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    
    # Limpiar signos
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    
    # Reemplazo por diccionario fonético
    corrected_tokens = [TYPO_DICTIONARY.get(tok, tok) for tok in tokens]
    normalized = " ".join(corrected_tokens)
    
    for typo, fix in TYPO_DICTIONARY.items():
        if " " in typo and typo in normalized:
            normalized = normalized.replace(typo, fix)
            
    return normalized.strip()

# Base estructurada de resolución autónoma obligatoria (Soporte Nivel 1)
TIER1_STRUCTURED_INTENTS = [
    # 1. Documentos y Requisitos Obligatorios para Matrícula
    {
        "intent": "registration_documents_and_requirements",
        "patterns": [
            r"\bdocumento\b", r"\bdocumentos\b", r"\bpapeles\b", r"\brequisito\b", r"\brequisitos\b",
            r"\bque me piden\b", r"\bque piden\b", r"\bque necesito para matricularme\b",
            r"\bque documentos piden\b", r"\bque documentos necesito\b", r"\bque papeles piden\b",
            r"\bque papeles necesito\b", r"\bpapeles pa matricula\b", r"\bdocumentos para matricula\b",
            r"\brequisitos de matricula\b", r"\brequisitos para entrar\b", r"\bdocumentos para inscribirme\b"
        ],
        "response": (
            "Para completar tu proceso de matrícula en LinguaColombia debes presentar la siguiente lista estandarizada de documentos:\n\n"
            "1. **Documento de identidad original:** Cédula de Ciudadanía, Tarjeta de Identidad o Cédula de Extranjería / Pasaporte vigente.\n"
            "2. **Comprobante de pago:** Recibo de pago de la matrícula completa o de la primera cuota (PSE, Nequi, Daviplata o Efecty).\n"
            "3. **Formulario de inscripción web:** Formato digital de datos del estudiante debidamente diligenciado en nuestra plataforma.\n"
            "4. **Prueba de nivelación (si aplica):** Certificado del Placement Test en caso de iniciar en un nivel superior al nivel inicial A1 Principiante.\n\n"
            "Todos estos documentos se adjuntan de forma 100% digital a través de nuestro portal de admisiones."
        )
    },
    # 2. Fallas Técnicas de Plataforma y Acceso al Aula Virtual (Fórmula de Diagnóstico Nivel 1)
    {
        "intent": "platform_technical_troubleshooting",
        "patterns": [
            r"\bno puedo ingresar\b", r"\bno puedo entrar\b", r"\bno abre la plataforma\b",
            r"\bno carga la plataforma\b", r"\bno carga la pagina\b", r"\bno me deja entrar\b",
            r"\bno me deja ingresar\b", r"\bno sirve la plataforma\b", r"\bno sirve la pagina\b",
            r"\bproblema para entrar\b", r"\berror al entrar\b", r"\berror al ingresar\b",
            r"\bquiero entrar a la clase\b", r"\bquiero ingresar a la clase\b", r"\bentrar a la clase\b",
            r"\bentrar a clase\b", r"\bentrar al curso\b", r"\bacceder a la clase\b", r"\bacceder al curso\b",
            r"\bentrar a mis clases\b", r"\bver la clase\b", r"\bno puedo ver la clase\b",
            r"\bplataforma caida\b", r"\bplataforma bloqueada\b", r"\bno abre el campus\b",
            r"\bolvide mi contrasena\b", r"\bolvide mi clave\b", r"\bno me llego el correo\b",
            r"\bno tengo acceso\b", r"\bcredenciales\b", r"\bclave de acceso\b"
        ],
        "response": (
            "Para solucionar de inmediato el acceso a tu Campus Virtual, sigue estos pasos de diagnóstico técnico:\n\n"
            "1. **Verificación de Conexión y Pestaña:** Comprueba tu conexión a internet y refresca la página presionando `Ctrl + F5`.\n"
            "2. **Limpieza del Navegador:** Borra cookies y archivos temporales de la memoria caché, o ingresa a través de una ventana en **Modo Incógnito** (Google Chrome, Edge o Firefox).\n"
            "3. **Validación de Credenciales:**\n"
            "   - **Usuario:** Tu correo electrónico registrado (asegúrate de no incluir espacios al inicio ni al final).\n"
            "   - **Contraseña:** Tu número de documento de identidad sin puntos ni guiones.\n"
            "4. **Restablecimiento de Clave:** Haz clic en el enlace *'¿Olvidaste tu contraseña?'* en el portal de ingreso para recibir el enlace de recuperación (revisa también tu carpeta de Spam).\n\n"
            "¿Pudiste acceder a tu aula virtual realizando estos 4 pasos?"
        )
    },
    # 3. Fallas y Problemas con el Pago (Diagnóstico Paso a Paso)
    {
        "intent": "payment_troubleshooting",
        "patterns": [
            r"\bno pude pagar\b", r"\bno puedo pagar\b", r"\bno me deja pagar\b", r"\bfallo el pago\b",
            r"\berror en el pago\b", r"\berror al pagar\b", r"\bproblema con el pago\b", r"\bproblemas con el pago\b",
            r"\brechazo el pago\b", r"\brechazo la tarjeta\b", r"\bno pasa la tarjeta\b", r"\bno paso la tarjeta\b",
            r"\bno me acepta el pago\b", r"\bno procesa el pago\b", r"\bno se pudo pagar\b", r"\bno pude hacer el pago\b",
            r"\bproblema con nequi\b", r"\bproblema con pse\b", r"\bproblema con daviplata\b", r"\bno me cobro\b"
        ],
        "response": (
            "Si presentaste una falla al momento de realizar tu pago, aplica la siguiente guía de resolución paso a paso:\n\n"
            "1. **Revisión de Permisos Bancarios:** Verifica que tu tarjeta de crédito/débito tenga habilitadas las compras virtuales y que tu cuenta PSE o Nequi cuente con saldo disponible.\n"
            "2. **Cambio de Canal de Pago:** Si la pasarela de pagos rechaza tu transacción, utiliza un medio alternativo directo:\n"
            "   - **Billetera Digital:** Transferencia directa por **Nequi** o **Daviplata**.\n"
            "   - **Efectivo Nacional:** Generación de recibo con código de convenio para pago en puntos **Efecty** o **Baloto**.\n"
            "3. **Financiación Inmediata:** Puedes diferir el valor de tu módulo a 3 cuotas con **0% de interés** seleccionando la opción **Addi** o **Sistecredito**.\n\n"
            "¿Cuál de estos medios prefieres utilizar para completar tu matrícula?"
        )
    },
    # 4. Costos, Tarifas y Opciones de Pago (Estructurado)
    {
        "intent": "pricing_and_discounts",
        "patterns": [
            r"\bprecio\b", r"\bprecios\b", r"\bcosto\b", r"\bcostos\b", r"\btarifa\b", r"\btarifas\b",
            r"\bcuanto vale\b", r"\bcuanto cuesta\b", r"\bvalor\b", r"\bvalores\b", r"\bdescuento\b",
            r"\bdescuentos\b", r"\bpromocion\b", r"\bpromociones\b", r"\boferta\b", r"\bpresupuesto\b"
        ],
        "response": (
            "A continuación te detallo la estructura oficial de costos y planes de pago en pesos colombianos (COP):\n\n"
            "1. **Modalidades y Tarifas por Módulo:**\n"
            "   - **Modalidad Estándar (Ciclo Mensual):** $680.000 COP por módulo (4 horas semanales de clase).\n"
            "   - **Modalidad Intensiva (Ciclo Acelerado):** $1.150.000 COP por módulo (8 horas semanales de lunes a jueves).\n"
            "2. **Descuentos Oficiales Aplicables:**\n"
            "   - **15% de Descuento:** Por pago anticipado de contado del nivel semestral completo (3 módulos).\n"
            "   - **10% de Descuento:** Para convenios corporativos o grupos familiares.\n"
            "3. **Facilidades de Financiación:** Aceptamos **PSE**, **Nequi**, **Daviplata**, tarjetas de crédito y cuotas al 0% de interés con **Addi** y **Sistecredito**.\n\n"
            "¿Deseas matricularte en la modalidad estándar o intensiva?"
        )
    },
    # 5. Medios y Canales de Pago en Colombia
    {
        "intent": "payment_methods",
        "patterns": [
            r"\bmedio de pago\b", r"\bmedios de pago\b", r"\bformas de pago\b", r"\bforma de pago\b",
            r"\bcomo pago\b", r"\bcomo pagar\b", r"\bpago\b", r"\bpagos\b", r"\bnequi\b", r"\bdaviplata\b",
            r"\bpse\b", r"\btarjeta\b", r"\btarjetas\b", r"\baddi\b", r"\bsistecredito\b", r"\befecty\b",
            r"\bbaloto\b", r"\btransferencia\b", r"\bbancolombia\b", r"\bdavivienda\b", r"\bcuotas\b", r"\bfinanciar\b"
        ],
        "response": (
            "Para realizar el pago de tu curso en LinguaColombia dispones de los siguientes canales oficiales:\n\n"
            "1. **Canales Digitales Inmediatos:**\n"
            "   - **PSE:** Débito directo desde cualquier cuenta bancaria en Colombia.\n"
            "   - **Billeteras Digitales:** Pagos instantáneos con **Nequi** y **Daviplata**.\n"
            "   - **Tarjetas:** Crédito y Débito (Visa, Mastercard, American Express).\n"
            "2. **Financiación a Cuotas sin Interés:** Hasta 3 cuotas con **0% de interés** mediante **Addi** y **Sistecredito**.\n"
            "3. **Pago en Efectivo a Nivel Nacional:** Puntos autorizados **Efecty** y **Baloto** presentando tu número de cédula y código de convenio.\n\n"
            "¿Deseas que te guíe para generar tu orden de pago digital?"
        )
    },
    # 6. Idiomas, Niveles y Duración
    {
        "intent": "languages_and_levels",
        "patterns": [
            r"\bidiomas\b", r"\bidioma\b", r"\bque idiomas\b", r"\bque cursos\b", r"\bcursos\b",
            r"\bingles\b", r"\bfrances\b", r"\baleman\b", r"\bnivel\b", r"\bniveles\b",
            r"\ba1\b", r"\ba2\b", r"\bb1\b", r"\bb2\b", r"\bc1\b", r"\bmcer\b", r"\bduracion\b",
            r"\bcuanto dura\b", r"\bcuanto tiempo\b", r"\bcuanto se demora\b", r"\bmeses\b"
        ],
        "response": (
            "Nuestra oferta académica está estructurada bajo el Marco Común Europeo de Referencia (MCER):\n\n"
            "1. **Idiomas Disponibles:** **Inglés**, **Francés** y **Alemán**.\n"
            "2. **Niveles de Formación:** Desde nivel **A1 (Principiante)** hasta nivel **C1 (Avanzado / Profesional)**.\n"
            "3. **Duración por Nivel según la Modalidad:**\n"
            "   - **Modalidad Estándar:** 4 meses por nivel (4 horas semanales de clase).\n"
            "   - **Modalidad Intensiva:** 2 meses por nivel (8 horas semanales, lunes a jueves).\n"
            "   - **Modalidad Superintensiva:** 1 mes por nivel (16 horas semanales para avance express).\n\n"
            "¿Te interesa estudiar Inglés, Francés o Alemán?"
        )
    },
    # 7. Horarios Disponibles (Mañana, Tarde, Noche y Sábados)
    {
        "intent": "schedules",
        "patterns": [
            r"\bhorario\b", r"\bhorarios\b", r"\bsabado\b", r"\bsabados\b", r"\bsabatino\b", r"\bsabatinos\b",
            r"\bfin de semana\b", r"\bfines de semana\b", r"\bmanana\b", r"\bmananas\b", r"\btarde\b",
            r"\btardes\b", r"\bnoche\b", r"\bnoches\b", r"\bque dias\b", r"\bque horas\b", r"\bjornada\b"
        ],
        "response": (
            "Disponemos de 4 franjas horarias flexibles para que elijas la que mejor se adapte a tu rutina:\n\n"
            "1. **Franja Mañana:** 6:00 a.m. - 8:00 a.m. | 8:00 a.m. - 10:00 a.m.\n"
            "2. **Franja Tarde:** 2:00 p.m. - 4:00 p.m. | 4:00 p.m. - 6:00 p.m.\n"
            "3. **Franja Noche:** 6:30 p.m. - 8:30 p.m. | 7:00 p.m. - 9:00 p.m.\n"
            "4. **Cursos Sabatinos:** Sábados de 8:00 a.m. - 12:00 m. o de 1:00 p.m. - 5:00 p.m.\n\n"
            "¿Prefieres tomar tus clases en semana o los días sábados?"
        )
    },
    # 8. Modalidades (Online vs Presencial)
    {
        "intent": "modalities",
        "patterns": [
            r"\bmodalidad\b", r"\bmodalidades\b", r"\bvirtual\b", r"\bonline\b", r"\ben vivo\b",
            r"\bpresencial\b", r"\bpresenciales\b", r"\bhibrido\b", r"\bhibrida\b", r"\bclases virtuales\b",
            r"\bcampus virtual\b"
        ],
        "response": (
            "Ofrecemos 3 modalidades de aprendizaje para todos nuestros cursos:\n\n"
            "1. **100% Online en Vivo:** Clases interactivas en tiempo real con docentes certificados y acceso 24/7 al Campus Virtual.\n"
            "2. **Presencial en Sede:** Aulas interactivas con laboratorios de audio y clubes de conversación presenciales.\n"
            "3. **Formato Híbrido (Flex-Class):** Combina sesiones presenciales con clases virtuales según tu disponibilidad semanal.\n\n"
            "¿En cuál de estas 3 modalidades deseas inscribirte?"
        )
    },
    # 9. Prueba de Nivelación Gratuita (Placement Test)
    {
        "intent": "placement_test",
        "patterns": [
            r"\bplacement test\b", r"\bplacement\b", r"\bprueba de nivelacion\b", r"\bexamen de nivelacion\b",
            r"\bexamen de clasificacion\b", r"\bprueba de clasificacion\b", r"\bnivelacion\b", r"\bclasificacion\b",
            r"\bdiagnostico\b", r"\bque nivel soy\b", r"\bsaber mi nivel\b", r"\bprueba gratis\b", r"\btest gratis\b",
            r"\bdonde hago el test\b", r"\blink del test\b", r"\blink del examen\b", r"\bhacer la prueba\b"
        ],
        "response": (
            "Para presentar tu **Prueba de Nivelación (Placement Test)** 100% gratuita, sigue estos pasos:\n\n"
            "1. **Test Escrito Online:** Ingresa a la sección de Admisiones y completa la prueba virtual de 25 a 35 minutos (evalúa gramática, lectura y comprensión auditiva).\n"
            "2. **Entrevista Oral de 10 minutos:** Agenda una breve sesión con un docente evaluador para medir tu fluidez.\n"
            "3. **Diagnóstico Inmediato:** Recibes tu informe con tu nivel exacto (A1 a C1) y el módulo recomendado para iniciar.\n\n"
            "¿Deseas presentar tu prueba de nivelación en este momento?"
        )
    },
    # 10. Certificaciones y Exámenes Oficiales
    {
        "intent": "certifications_and_exams",
        "patterns": [
            r"\bexamen oficial\b", r"\bexamenes oficiales\b", r"\bcertificacion\b", r"\bcertificaciones\b",
            r"\bielts\b", r"\btoefl\b", r"\bdelf\b", r"\bdalf\b", r"\bgoethe\b", r"\bcambridge\b",
            r"\bfce\b", r"\bcae\b", r"\bdiploma\b", r"\bcertificado\b", r"\bsimulacro\b", r"\bsimulacros\b"
        ],
        "response": (
            "Somos centro de preparación autorizado para los siguientes exámenes oficiales:\n\n"
            "1. **Inglés:** **IELTS** (Academic y General), **TOEFL iBT** y certificaciones Cambridge (**B2 First / C1 Advanced**).\n"
            "2. **Francés:** **DELF / DALF** (certificación oficial del Ministerio de Educación de Francia).\n"
            "3. **Alemán:** **Goethe-Zertifikat** (niveles A1 a C1 para trámites de estudio o visa).\n"
            "4. **Simulacros Reales:** Todos los cursos incluyen **3 simulacros reales cronometrados** y estrategias de examen.\n\n"
            "¿Para cuál de estos exámenes internacionales necesitas prepararte?"
        )
    },
    # 11. Proceso de Matrícula e Inscripción
    {
        "intent": "enrollment_process",
        "patterns": [
            r"\binscripcion\b", r"\binscripciones\b", r"\bmatricula\b", r"\bmatriculas\b",
            r"\bcomo me inscribo\b", r"\bcomo matricularme\b", r"\bpasos de matricula\b",
            r"\bcomo empezar\b", r"\bfechas de inicio\b", r"\bcuando inician\b", r"\bquiero inscribirme\b",
            r"\bquiero matricularme\b"
        ],
        "response": (
            "El proceso de matrícula es 100% digital y se completa en 3 simples pasos:\n\n"
            "1. **Diagnóstico de Nivel:** Realiza el Placement Test gratuito o selecciona iniciar desde el nivel A1 Principiante.\n"
            "2. **Formulario de Admisión:** Diligencia tus datos básicos y documento de identidad en el formulario web.\n"
            "3. **Pago y Activación:** Realiza el pago en línea mediante PSE, Nequi, tarjeta o Addi. Recibirás de inmediato tus credenciales del Campus Virtual.\n\n"
            "¡Iniciamos nuevos grupos todas las semanas! ¿En qué idioma deseas matricularte?"
        )
    },
    # 12. Saludos y Llamados a Poly
    {
        "intent": "greeting",
        "patterns": [
            r"^poly$", r"^poli$", r"^poly\b", r"^poli\b", r"^hola\b", r"^ola\b", r"^buenas\b",
            r"^buenos dias\b", r"^buenas tardes\b", r"^buenas noches\b", r"^hey\b",
            r"^que tal\b", r"^saludos\b", r"^como estas\b", r"^como te va\b", r"^buen dia\b",
            r"^holis\b", r"^alo\b", r"^inicio\b", r"^empezar\b", r"^hola poly\b", r"^ola poly\b",
            r"^hey poly\b", r"^poly hola\b", r"^poly ayudame\b", r"^asistente\b"
        ],
        "response": (
            "¡Hola! 👋 Qué gusto saludarte. Soy **Poly**, tu asistente virtual oficial de LinguaColombia.\n\n"
            "Estoy aquí para responder todas tus preguntas sobre nuestros programas de **Inglés, Francés y Alemán**, "
            "modalidades, horarios, documentos de matrícula, formas de pago y certificaciones.\n\n"
            "¿En qué te gustaría que te oriente hoy?"
        )
    },
    # 13. Devoluciones, Congelaciones y Aplazamientos
    {
        "intent": "refunds_and_freezing",
        "patterns": [
            r"\bdevolucion\b", r"\bdevoluciones\b", r"\breembolso\b", r"\breembolsos\b",
            r"\bcancelar curso\b", r"\bcongelar curso\b", r"\bcongelar matricula\b",
            r"\bretirarme\b", r"\baplazar\b", r"\baplazamiento\b", r"\bcongelar\b"
        ],
        "response": (
            "El reglamento estudiantil de LinguaColombia establece las siguientes políticas de gestión académica:\n\n"
            "1. **Congelación de Curso:** Puedes congelar tu nivel hasta por un máximo de **6 meses** sin costo alguno, notificando con 3 días hábiles de anticipación al inicio del módulo.\n"
            "2. **Reembolsos:** Aplican únicamente antes del inicio de las clases con una deducción del 10% por gastos administrativos.\n\n"
            "¿Deseas tramitar la congelación de tu módulo o verificar las fechas de inicio?"
        )
    },
    # 14. Metodología, Profesores y Materiales
    {
        "intent": "methodology_and_teachers",
        "patterns": [
            r"\bprofesores\b", r"\bdocentes\b", r"\bnativos\b", r"\bprofes\b", r"\bmetodologia\b",
            r"\bcomo son las clases\b", r"\blibros\b", r"\bmateriales\b", r"\bplataforma\b", r"\bclub de conversacion\b"
        ],
        "response": (
            "Nuestra metodología de enseñanza garantiza un aprendizaje comunicativo e inmersivo:\n\n"
            "1. **Docentes Calificados:** Profesores licenciados y certificados internacionalmente (C1/C2 y docentes nativos).\n"
            "2. **Grupos Reducidos:** Máximo 12 estudiantes por aula para asegurar participación activa.\n"
            "3. **Materiales Incluidos:** Libros digitales, audios y talleres interactivos 100% incluidos en el valor de la matrícula.\n"
            "4. **Clubes de Conversación:** Acceso libre semanal a talleres de pronunciación y debates en vivo.\n\n"
            "¿En qué idioma te gustaría conocer la metodología?"
        )
    },
    # 15. Identidad y capacidades
    {
        "intent": "identity",
        "patterns": [
            r"^quien eres\b", r"^quien es poly\b", r"^que haces\b", r"^que puedes hacer\b",
            r"^como me puedes ayudar\b", r"^de que trata\b", r"^que eres\b", r"^presentate\b",
            r"^que es linguacolombia\b", r"^para que sirves\b", r"^cual es tu funcion\b",
            r"^quien te creo\b", r"^como te llamas\b", r"^cual es tu nombre\b"
        ],
        "response": (
            "¡Mucho gusto! Soy **Poly**, la asistente virtual oficial de **LinguaColombia**. 🇨🇴\n\n"
            "Puedo ayudarte a resolver tus dudas sobre:\n"
            "1. **Programas e Idiomas:** Inglés, Francés y Alemán (Niveles A1 a C1 según el Marco Común Europeo).\n"
            "2. **Precios y Descuentos:** Tarifas por módulo en COP, 15% de descuento por nivel completo y financiación al 0% con Addi/Sistecredito.\n"
            "3. **Documentos de Matrícula:** Cédula, comprobante de pago, formulario y placement test.\n"
            "4. **Medios de Pago:** PSE, Nequi, Daviplata, tarjetas de crédito y puntos Efecty/Baloto.\n"
            "5. **Horarios y Modalidades:** Clases online en vivo, presenciales y cursos sabatinos.\n"
            "6. **Admisiones:** Placement Test gratuito y preparación para exámenes (IELTS, TOEFL, DELF, Goethe).\n\n"
            "¿Sobre cuál de estos temas deseas consultar?"
        )
    },
    # 16. Agradecimientos
    {
        "intent": "gratitude",
        "patterns": [
            r"^gracias\b", r"^muchas gracias\b", r"^te agradezco\b", r"^mil gracias\b",
            r"^excelente gracias\b", r"^muy amable\b", r"^ok gracias\b", r"^listo gracias\b",
            r"^perfecto gracias\b", r"^muchisimas gracias\b", r"^vale gracias\b", r"^super gracias\b",
            r"^muchas gracias poly\b", r"^gracias poly\b", r"^gracias por la informacion\b"
        ],
        "response": (
            "¡Con el mayor de los gustos! 😊 En LinguaColombia estamos listos para acompañarte en tu meta de dominar un nuevo idioma.\n\n"
            "Si tienes cualquier otra pregunta sobre horarios, niveles o formas de pago, aquí estaré. ¡Que tengas un excelente día!"
        )
    },
    # 17. Despedidas
    {
        "intent": "farewell",
        "patterns": [
            r"^chao\b", r"^adios\b", r"^hasta luego\b", r"^nos vemos\b", r"^hasta pronto\b",
            r"^bye\b", r"^chao gracias\b", r"^que estes bien\b", r"^hasta la proxima\b",
            r"^feliz dia\b", r"^feliz tarde\b", r"^feliz noche\b", r"^buen descanso\b"
        ],
        "response": (
            "¡Hasta pronto! 👋 Recuerda que en LinguaColombia abrimos ciclos de matrícula todos los meses.\n\n"
            "Si más adelante deseas iniciar tu inscripción o agendar tu prueba de nivelación gratuita, con gusto te orientaré. ¡Muchos éxitos!"
        )
    },
    # 18. Menú de ayuda general
    {
        "intent": "help_menu",
        "patterns": [
            r"^ayuda\b", r"^opciones\b", r"^menu\b", r"^que opciones hay\b",
            r"^informacion general\b", r"^asesoria\b", r"^necesito ayuda\b",
            r"^no se que preguntar\b", r"^que me recomiendas\b", r"^guia\b"
        ],
        "response": (
            "¡Claro que sí! Con gusto te oriento. Puedes preguntarme directamente sobre:\n\n"
            "1. **Precios y Financiación:** Tarifas por módulo, 15% de descuento y cuotas con Addi/Sistecredito.\n"
            "2. **Documentos de Matrícula:** Requisitos estandarizados de inscripción.\n"
            "3. **Idiomas y Niveles:** Cursos de Inglés, Francés y Alemán (A1 a C1).\n"
            "4. **Horarios y Sabatinos:** Franjas de mañana, tarde, noche y fines de semana.\n"
            "5. **Prueba de Nivelación Gratuita:** Diagnóstico pedagógico en 25 minutos.\n"
            "6. **Exámenes Oficiales:** Preparación para IELTS, TOEFL, DELF y Goethe.\n\n"
            "¿Sobre cuál de estos temas deseas consultar?"
        )
    }
]

def check_conversational_intent(query: str) -> Optional[Dict[str, Any]]:
    """
    Evalúa la consulta con preprocesamiento semántico tolerante a errores ortográficos,
    repetición de letras y patrones de soporte técnico de Nivel 1.
    """
    clean_q = clean_and_normalize(query)
    if not clean_q:
        return None

    for item in TIER1_STRUCTURED_INTENTS:
        for pattern in item["patterns"]:
            if re.search(pattern, clean_q):
                return {
                    "intent": item["intent"],
                    "answer": item["response"],
                    "is_escalated": False,
                    "confidence_score": 1.0,
                    "model_used": "Poly Tier-1 Support Engine"
                }
    return None
