import React, { useState } from 'react';
import { HelpCircle, BookOpen, DollarSign, Clock, Award, MessageCircle, ChevronDown, ChevronUp } from 'lucide-react';

const SUGGESTIONS = [
  {
    icon: BookOpen,
    label: "Idiomas y Niveles",
    query: "¿Qué idiomas enseñan, qué niveles manejan y cuánto dura cada ciclo?"
  },
  {
    icon: DollarSign,
    label: "Precios y Descuentos",
    query: "¿Cuánto cuesta el módulo en pesos colombianos y tienen descuentos por pago de contado?"
  },
  {
    icon: DollarSign,
    label: "Medios de Pago",
    query: "¿Puedo pagar con Nequi, PSE o financiar a cuotas con Addi?"
  },
  {
    icon: Clock,
    label: "Horarios y Modalidades",
    query: "¿Tienen cursos sabatinos y qué modalidades de estudio ofrecen?"
  },
  {
    icon: Award,
    label: "Prueba de Nivelación",
    query: "¿Cómo es el examen de nivelación gratuito y preparan para el examen IELTS o TOEFL?"
  },
  {
    icon: MessageCircle,
    label: "Otras Consultas",
    query: "¿Ofrecen cursos de cocina italiana o repostería los fines de semana?"
  }
];

export default function SuggestionChips({ onSelectQuery, disabled }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = (query) => {
    onSelectQuery(query);
    setIsOpen(false);
  };

  return (
    <div className="w-full max-w-4xl mx-auto py-1">
      {/* Accordion Toggle Header */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="group flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-white dark:bg-slate-900 hover:bg-cyan-50/70 dark:hover:bg-slate-800 text-slate-800 dark:text-slate-200 hover:text-cyan-700 dark:hover:text-cyan-300 border border-slate-200 dark:border-slate-800 hover:border-cyan-400 dark:hover:border-cyan-500/40 transition-all text-xs font-semibold shadow-sm"
        >
          <div className="p-0.5 rounded text-cyan-600 dark:text-cyan-400 group-hover:scale-110 transition-transform">
            <HelpCircle className="w-3.5 h-3.5" />
          </div>
          <span>Preguntas Frecuentes</span>
          <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-mono font-bold">
            6
          </span>
          <span className="text-slate-400 group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors ml-0.5">
            {isOpen ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </span>
        </button>

        {isOpen && (
          <span className="text-[11px] text-slate-600 dark:text-slate-400 hidden sm:inline font-medium">
            Selecciona una opción para consultar a Poly
          </span>
        )}
      </div>

      {/* Accordion Expandable Body in Pure White with Cyan Highlights */}
      {isOpen && (
        <div className="mt-2.5 p-3 rounded-2xl bg-white dark:bg-[#0f172a] border border-slate-200 dark:border-slate-800 shadow-xl shadow-slate-200/60 dark:shadow-2xl dark:shadow-black/50 backdrop-blur-md animate-fadeIn">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
            {SUGGESTIONS.map((item, idx) => {
              const Icon = item.icon;

              return (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelect(item.query)}
                  disabled={disabled}
                  className={`group text-left p-3 rounded-xl text-xs transition-all duration-200 border flex items-start gap-2.5 bg-slate-50/90 dark:bg-slate-950/70 hover:bg-white dark:hover:bg-slate-900 border-slate-200 dark:border-slate-800 hover:border-cyan-400 dark:hover:border-cyan-500/40 text-slate-800 dark:text-slate-200 hover:shadow-md ${
                    disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:scale-[1.01] active:scale-[0.99]'
                  }`}
                >
                  <div className="p-1.5 rounded-lg bg-cyan-50 dark:bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 group-hover:bg-cyan-500 group-hover:text-white transition-all duration-200 flex-shrink-0 mt-0.5">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <div className="flex flex-col overflow-hidden">
                    <span className="font-bold text-slate-900 dark:text-white group-hover:text-cyan-700 dark:group-hover:text-cyan-400 transition-colors line-clamp-1">
                      {item.label}
                    </span>
                    <span className="text-[11px] text-slate-600 dark:text-slate-400 font-normal line-clamp-2 leading-relaxed mt-0.5">
                      {item.query}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
