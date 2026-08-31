import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp } from 'lucide-react';

export default function EvidenceViewer({ citations, isOpen, onToggle }) {
  const [expandedChunk, setExpandedChunk] = useState(null);

  if (!citations || citations.length === 0) return null;

  const cleanSectionTitle = (title) => {
    if (!title) return "Información Oficial";
    return title.replace(/^\d+[\.\-_\s]*/, '').trim();
  };

  return (
    <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800/80">
      {/* Botón Principal del Acordeón */}
      <button
        type="button"
        onClick={onToggle}
        className="flex items-center justify-between w-full text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-cyan-600 dark:hover:text-cyan-400 py-1 transition-colors"
      >
        <span className="flex items-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" />
          <span>Ver fuentes oficiales consultadas ({citations.length})</span>
        </span>
        <span className="flex items-center gap-1 text-slate-400 text-[11px]">
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </span>
      </button>

      {/* Lista de Fuentes Oficiales Limpia */}
      {isOpen && (
        <div className="mt-2.5 space-y-2 animate-fadeIn">
          {citations.map((cite, idx) => {
            const isExpanded = expandedChunk === idx;
            const cleanTitle = cleanSectionTitle(cite.section);

            return (
              <div
                key={idx}
                className="rounded-xl bg-slate-50 dark:bg-slate-950/70 border border-slate-200/90 dark:border-slate-800/90 p-3 text-xs text-slate-700 dark:text-slate-300 hover:border-cyan-300 dark:hover:border-cyan-500/40 transition-all shadow-sm"
              >
                <div 
                  className="flex items-center justify-between cursor-pointer gap-2"
                  onClick={() => setExpandedChunk(isExpanded ? null : idx)}
                >
                  <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 flex-shrink-0" />
                    <span className="font-semibold text-slate-900 dark:text-slate-200 text-xs">
                      {cleanTitle}
                    </span>
                  </div>

                  <button 
                    type="button"
                    className="text-[11px] text-cyan-600 dark:text-cyan-400 hover:underline flex items-center gap-1 flex-shrink-0 font-medium"
                  >
                    <span>{isExpanded ? 'Ocultar' : 'Ver detalle'}</span>
                    {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  </button>
                </div>

                {isExpanded && (
                  <div className="mt-2 pt-2 border-t border-slate-200 dark:border-slate-800/60 text-slate-700 dark:text-slate-300 font-sans leading-relaxed text-[11.5px] bg-white dark:bg-slate-900/50 p-2.5 rounded-lg border border-slate-100 dark:border-transparent">
                    <p className="whitespace-pre-wrap">{cite.snippet}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
