#!/usr/bin/env python3
"""
Script generador del corpus documental oficial para la Academia de Idiomas LinguaColombia.
Genera documentos estructurados en HTML con información verídica y detallada
sobre programas, niveles CEFR, modalidades, precios en COP, medios de pago en Colombia,
horarios, exámenes oficiales y procesos de matrícula.
"""

import os
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"

DOC_1_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>01 - Programas Académicos, Idiomas y Niveles - LinguaColombia</title>
</head>
<body>
    <header>
        <h1>Academia de Idiomas LinguaColombia: Catálogo de Programas y Niveles</h1>
        <p><strong>Código de Documento:</strong> DOC-ACAD-001 | <strong>Vigencia:</strong> 2026</p>
    </header>

    <section id="idiomas-ofertados">
        <h2>1. Idiomas Disponibles</h2>
        <p>LinguaColombia ofrece formación profesional en tres idiomas de alta demanda global y laboral:</p>
        <ul>
            <li><strong>Inglés General y Profesional:</strong> Enfoque comunicativo integral, desarrollo de fluidez, comprensión auditiva, redacción corporativa y preparación académica.</li>
            <li><strong>Francés Francófono:</strong> Enfoque comunicativo y cultural, orientado a estudios en Francia/Canadá (proceso Québec) y certificaciones DELF/DALF.</li>
            <li><strong>Alemán Estándar (Hochdeutsch):</strong> Formación estructurada para oportunidades laborales, homologación de títulos y estudios universitarios en Alemania, Austria y Suiza.</li>
        </ul>
    </section>

    <section id="marco-europeo">
        <h2>2. Estructura de Niveles según el Marco Común Europeo (MCER / CEFR)</h2>
        <p>Todos nuestros programas están alineados estrictamente con el Marco Común Europeo de Referencia para las Lenguas:</p>
        <ul>
            <li><strong>Nivel A1 (Acceso / Principiante):</strong> Capacidad de comprender y utilizar expresiones cotidianas básicas y frases sencillas dirigidas a satisfacer necesidades de tipo inmediato. Presentarse a sí mismo y a otros.</li>
            <li><strong>Nivel A2 (Plataforma / Elemental):</strong> Comprensión de frases y expresiones frecuentes sobre áreas de relevancia inmediata (familia, compras, lugares de interés, ocupación). Intercambios sencillos y directos.</li>
            <li><strong>Nivel B1 (Umbral / Pre-Intermedio):</strong> Desenvolvimiento en la mayor parte de situaciones cotidianas y viajes. Producción de textos sencillos y coherentes sobre temas familiares o de interés personal.</li>
            <li><strong>Nivel B2 (Avanzado / Intermedio-Alto):</strong> Comprensión de ideas principales de textos complejos técnicos o literarios. Fluidez y naturalidad en conversaciones con hablantes nativos sin tensión.</li>
            <li><strong>Nivel C1 (Dominio Operativo Eficaz):</strong> Expresión fluida y espontánea sin esfuerzo evidente. Uso flexible y efectivo del idioma para fines sociales, académicos y profesionales.</li>
        </ul>
    </section>

    <section id="modalidades">
        <h2>3. Modalidades de Estudio</h2>
        <p>Los estudiantes pueden elegir entre tres modalidades flexibles según su ubicación y disponibilidad:</p>
        <ul>
            <li><strong>100% Online en Vivo (Campus Virtual Lingua):</strong> Clases sincrónicas en tiempo real a través de nuestra plataforma interactiva con docentes nativos o bilingües certificados. Grupos reducidos (máximo 8 estudiantes por aula virtual). Incluye acceso 24/7 a grabaciones y recursos multimedia.</li>
            <li><strong>Presencial Tradicional:</strong> Impartida en nuestras sedes físicas dotadas de laboratorios multimedia de audio e inmersión lingüística:
                <ul>
                    <li><strong>Sede Bogotá:</strong> Chapinero Central (Carrera 7 con Calle 53) y Sede Norte Calle 100 (Carrera 15 con Calle 98).</li>
                    <li><strong>Sede Medellín:</strong> El Poblado (Milla de Oro, Cra 43A) y Laureles (Avenida Nutibara).</li>
                </ul>
            </li>
            <li><strong>Modalidad Híbrida (Flex-Class):</strong> Combina 2 días presenciales en sede y 2 días sincrónicos virtuales por semana, permitiendo balance entre inmersión física y comodidad digital.</li>
        </ul>
    </section>

    <section id="duracion-ciclos">
        <h2>4. Duración de los Ciclos y Ritmo de Aprendizaje</h2>
        <p>Cada nivel del MCER (A1, A2, B1, B2, C1) se divide en 3 módulos secuenciales (ej. B1.1, B1.2, B1.3). La duración depende del ritmo seleccionado:</p>
        <ul>
            <li><strong>Modalidad Estándar:</strong> 4 horas semanales de clase. Duración de 4 meses por cada nivel completo (aprox. 64 horas académicas por nivel). Ideal para profesionales y estudiantes universitarios en horario nocturno o sabatino.</li>
            <li><strong>Modalidad Intensiva:</strong> 8 horas semanales de clase (2 horas diarias de lunes a jueves). Duración de 2 meses por cada nivel completo. Enfoque acelerado con práctica conversacional diaria.</li>
            <li><strong>Modalidad Superintensivo / Inmersión:</strong> 16 horas semanales (4 horas diarias de lunes a jueves). Duración de 1 mes por cada nivel completo. Recomendado para personas con planes de viaje o becas inmediatas.</li>
        </ul>
    </section>
</body>
</html>
"""

DOC_2_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>02 - Tarifas en COP, Medios de Pago y Horarios - LinguaColombia</title>
</head>
<body>
    <header>
        <h1>Academia de Idiomas LinguaColombia: Tarifas, Opciones de Pago y Franjas Horarias</h1>
        <p><strong>Código de Documento:</strong> DOC-FIN-002 | <strong>Moneda:</strong> Pesos Colombianos (COP) | <strong>Vigencia:</strong> 2026</p>
    </header>

    <section id="tarifas-precios">
        <h2>1. Estructura de Tarifas por Nivel y Módulo (Precios en COP)</h2>
        <p>Nuestras tarifas incluyen material digital interactivo, acceso a la plataforma de autoestudio 24/7 y clubes de conversación semanales ilimitados:</p>
        <ul>
            <li><strong>Curso Estándar (por Módulo individual):</strong> $680.000 COP. Cada nivel completo consta de 3 módulos.</li>
            <li><strong>Curso Intensivo (por Módulo individual):</strong> $1.150.000 COP. Acelerado con mayor intensidad horaria semanal.</li>
            <li><strong>Curso Superintensivo (Nivel completo en 1 mes):</strong> $2.890.000 COP.</li>
            <li><strong>Clubes de Conversación y Refuerzo Gramatical:</strong> Gratuitos e incluidos para todos los alumnos activos matriculados.</li>
            <li><strong>Kit de Libros Físicos (Opcional para cursos presenciales):</strong> $160.000 COP (el material en formato digital e-book ya está 100% incluido en la matrícula).</li>
        </ul>
    </section>

    <section id="descuentos-financiamiento">
        <h2>2. Descuentos Especiales y Financiamiento</h2>
        <p>Para facilitar el acceso a la educación en idiomas, disponemos de los siguientes incentivos económicos:</p>
        <ul>
            <li><strong>Descuento por Pago Anticipado de Nivel Completo:</strong> 15% de descuento al cancelar de contado los 3 módulos del nivel en un solo pago.</li>
            <li><strong>Descuento Familiar / Empresarial:</strong> 10% de descuento adicional por matricular a dos o más miembros del mismo núcleo familiar o mediante convenios corporativos vigentes.</li>
            <li><strong>Descuento por Continuidad:</strong> 5% de descuento en el siguiente nivel al mantener un promedio académico superior al 90% (4.5/5.0).</li>
            <li><strong>Opciones de Financiación sin Interés:</strong>
                <ul>
                    <li>Alianza directa con <strong>Addi</strong> y <strong>Sistecredito</strong>: Paga hasta en 3 cuotas con 0% de interés y aprobación inmediata con cédula de ciudadanía.</li>
                    <li>Crédito directo con LinguaColombia: 50% al iniciar y 50% a los 30 días calendario sin recargo de intereses.</li>
                </ul>
            </li>
        </ul>
    </section>

    <section id="medios-de-pago">
        <h2>3. Medios de Pago Habilitados en Colombia</h2>
        <p>Aceptamos los canales de recaudo más populares y seguros de Colombia:</p>
        <ul>
            <li><strong>PSE (Pagos Seguros en Línea):</strong> Débito inmediato desde cualquier cuenta de ahorros o corriente en entidades bancarias colombianas.</li>
            <li><strong>Billeteras Digitales:</strong> Pagos directos mediante código QR o número de convenio en <strong>Nequi</strong> y <strong>Daviplata</strong>.</li>
            <li><strong>Tarjetas de Crédito y Débito:</strong> Visa, Mastercard, American Express y Diners Club (diferible desde 1 hasta 36 cuotas).</li>
            <li><strong>Transferencia Bancaria Directa:</strong> Cuentas corrientes oficiales en Bancolombia y Banco Davivienda (envío de comprobante a tesorería).</li>
            <li><strong>Pago en Efectivo / Puntos de Recaudo:</strong> Convenio nacional con puntos <strong>Efecty</strong>, <strong>Baloto</strong> y <strong>Gana</strong> presentando el número de factura de matrícula.</li>
        </ul>
    </section>

    <section id="horarios-disponibles">
        <h2>4. Franjas Horarias Disponibles</h2>
        <p>Contamos con amplia disponibilidad horaria tanto en modalidad online como presencial en Bogotá y Medellín:</p>
        <ul>
            <li><strong>Franja Mañanas (Lunes a Jueves):</strong>
                <ul>
                    <li>Primer turno: 6:00 AM a 8:00 AM (Ideal antes de la jornada laboral).</li>
                    <li>Segundo turno: 8:30 AM a 10:30 AM.</li>
                </ul>
            </li>
            <li><strong>Franja Tardes (Lunes a Jueves):</strong>
                <ul>
                    <li>Turno único: 2:00 PM a 4:00 PM o 4:30 PM a 6:30 PM.</li>
                </ul>
            </li>
            <li><strong>Franja Noches (Lunes a Jueves):</strong>
                <ul>
                    <li>Primer turno nocturno: 6:30 PM a 8:30 PM.</li>
                    <li>Segundo turno nocturno: 8:00 PM a 10:00 PM.</li>
                </ul>
            </li>
            <li><strong>Cursos Sabatinos (Sábados):</strong>
                <ul>
                    <li>Sabatino Mañana: 8:00 AM a 12:00 PM (4 horas de clase con pausa activa de 20 minutos).</li>
                    <li>Sabatino Tarde: 1:00 PM a 5:00 PM (4 horas de clase con pausa activa de 20 minutos).</li>
                </ul>
            </li>
        </ul>
    </section>
</body>
</html>
"""

DOC_3_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>03 - Certificaciones Internacionales, Examen de Nivelación y Matrículas - LinguaColombia</title>
</head>
<body>
    <header>
        <h1>Academia de Idiomas LinguaColombia: Proceso de Admisión, Nivelación y Exámenes Oficiales</h1>
        <p><strong>Código de Documento:</strong> DOC-ADM-003 | <strong>Vigencia:</strong> 2026</p>
    </header>

    <section id="prueba-nivelacion">
        <h2>1. Prueba de Nivelación Gratuita (Placement Test)</h2>
        <p>Para garantizar que cada estudiante comience en el nivel adecuado a sus competencias reales:</p>
        <ul>
            <li><strong>Costo:</strong> 100% gratuita y sin compromiso de matrícula.</li>
            <li><strong>Metodología:</strong> Consta de dos etapas:
                <ol>
                    <li>Test Online Automatizado (Gramática, vocabulario y comprensión lectora/auditiva): Duración aproximada de 25 a 35 minutos en nuestro portal web.</li>
                    <li>Entrevista Oral Breve (Speaking de 10 minutos): Realizada por videollamada o presencial con un docente evaluador para validar fluidez y pronunciación.</li>
                </ol>
            </li>
            <li><strong>Resultados:</strong> Emisión inmediata del diagnóstico pedagógico con el nivel MCER recomendado y plan de estudio sugerido.</li>
            <li><strong>Principiantes Absolutos:</strong> Quienes no tengan conocimientos previos pueden iniciar directamente en el Nivel A1.1 sin presentar la prueba.</li>
        </ul>
    </section>

    <section id="certificaciones-internacionales">
        <h2>2. Preparación para Exámenes Oficiales Internacionales</h2>
        <p>LinguaColombia es centro autorizado de preparación para las pruebas de certificación de mayor reconocimiento internacional:</p>
        <ul>
            <li><strong>Certificaciones de Inglés:</strong>
                <ul>
                    <li><strong>IELTS (International English Language Testing System):</strong> Modalidades Academic y General Training. Módulos especializados en técnicas de respuesta para las bandas 6.5 a 8.5+.</li>
                    <li><strong>TOEFL iBT (Test of English as a Foreign Language):</strong> Preparación orientada a admisiones universitarias en Norteamérica y posgrados.</li>
                    <li><strong>Cambridge English Qualifications:</strong> Preparación para B2 First (FCE) y C1 Advanced (CAE).</li>
                </ul>
            </li>
            <li><strong>Certificaciones de Francés:</strong>
                <ul>
                    <li><strong>DELF / DALF:</strong> Diplomas otorgados por el Ministerio de Educación de Francia (Niveles A1 a C1).</li>
                    <li><strong>TCF Québec / TCF Canada:</strong> Preparación específica en expresión y comprensión oral para procesos migratorios.</li>
                </ul>
            </li>
            <li><strong>Certificaciones de Alemán:</strong>
                <ul>
                    <li><strong>Goethe-Zertifikat:</strong> Exámenes del Goethe-Institut reconocidos mundialmente (Niveles A1 a C1). Requisito para visas de trabajo o estudio en Alemania.</li>
                    <li><strong>TestDaF:</strong> Examen de idioma para acceso a universidades alemanas.</li>
                </ul>
            </li>
            <li><strong>Simulacros y Talleres:</strong> Todos los cursos de preparación incluyen 3 simulacros completos con retroalimentación personalizada de puntuación.</li>
        </ul>
    </section>

    <section id="proceso-matricula">
        <h2>3. Proceso de Inscripción y Matrícula Paso a Paso</h2>
        <p>El registro se realiza en cuatro sencillos pasos de manera virtual o presencial:</p>
        <ol>
            <li><strong>Paso 1 - Registro y Diagnóstico:</strong> Diligenciar el formulario web del aspirante y realizar el Placement Test gratuito si se poseen conocimientos previos.</li>
            <li><strong>Paso 2 - Selección de Horario y Modalidad:</strong> Elegir la sede física (Bogotá / Medellín) o Campus Virtual 100% Online, junto con la franja horaria preferida (semana o sabatino).</li>
            <li><strong>Paso 3 - Liquidación y Pago:</strong> Generar la orden de pago y cancelar mediante PSE, Nequi, Daviplata, tarjeta o crédito Addi/Sistecredito.</li>
            <li><strong>Paso 4 - Activación y Bienvenida:</strong> Recepción de credenciales de acceso al Campus Virtual, asignación de docente titular y sesión de inducción 24 horas antes del inicio de clases.</li>
        </ol>
    </section>

    <section id="fechas-calendario">
        <h2>4. Fechas de Inicio y Cortes de Matrícula Mensual</h2>
        <p>Mantenemos ciclos de apertura continuos durante todo el año académico:</p>
        <ul>
            <li><strong>Inicios de Ciclo Mensual:</strong>
                <ul>
                    <li><strong>Primer ciclo del mes:</strong> Inicia el primer lunes hábil de cada mes.</li>
                    <li><strong>Segundo ciclo del mes:</strong> Inicia el tercer lunes hábil de cada mes.</li>
                    <li><strong>Ciclos Sabatinos:</strong> Inician el primer y tercer sábado de cada mes.</li>
                </ul>
            </li>
            <li><strong>Cierre de Matrículas:</strong> El proceso de matrícula ordinaria cierra 3 días hábiles antes de la fecha de inicio del ciclo respectivo.</li>
            <li><strong>Matrícula Extraordinaria:</strong> Sujeta a disponibilidad de cupos con un recargo administrativo del 5% hasta el día anterior al inicio de clases.</li>
            <li><strong>Cupos Limitados:</strong> Máximo 8 estudiantes por aula virtual y 12 estudiantes en sedes presenciales para garantizar atención personalizada.</li>
        </ul>
    </section>
</body>
</html>
"""

def generate_corpus():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    files = [
        ("01_programas_y_niveles.html", DOC_1_CONTENT),
        ("02_tarifas_horarios_y_pagos.html", DOC_2_CONTENT),
        ("03_certificaciones_e_inscripciones.html", DOC_3_CONTENT)
    ]
    
    print(f"[*] Generando corpus documental en: {DOCS_DIR}")
    for filename, content in files:
        filepath = DOCS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"  [+] Documento creado: {filename} ({len(content)} caracteres)")

    print("[✓] Corpus documental generado exitosamente con 3 documentos oficiales.")

if __name__ == "__main__":
    generate_corpus()
