import React from 'react';
import { Settings, RefreshCw } from 'lucide-react';

export default function Header({ 
  health, 
  onOpenSettings, 
  onClearChat
}) {
  return (
    <header className="sticky top-0 z-30 backdrop-blur-md bg-[#091322]/90 border-b border-slate-800/80 px-4 lg:px-8 py-3 shadow-md shadow-black/20">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-4">
        
        {/* Brand & Logo with Poly Hover Zoom Effect */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center group cursor-pointer">
            <div className="w-10 h-10 flex items-center justify-center">
              <img 
                src="/poly.png" 
                alt="Poly Avatar" 
                className="w-full h-full object-contain filter drop-shadow-[0_2px_6px_rgba(6,182,212,0.4)] transition-all duration-300 ease-out group-hover:scale-135 group-hover:rotate-6 group-hover:drop-shadow-[0_4px_12px_rgba(6,182,212,0.7)]"
                title="Poly • Asistente Virtual"
              />
            </div>
            {/* Active Status Ping */}
            <span className="absolute -bottom-0.5 -right-0.5 flex h-3 w-3 pointer-events-none">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500 ring-2 ring-slate-950"></span>
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-bold text-lg tracking-tight text-white">
                Poly
              </h1>
              <span className="text-[11px] font-semibold text-cyan-400 bg-cyan-500/10 px-2.5 py-0.5 rounded-full border border-cyan-500/20">
                Asistente Virtual
              </span>
            </div>
            <p className="text-xs font-medium text-slate-400">
              LinguaColombia • Atención Oficial
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          
          {/* Button: Settings (Ajustes) */}
          <button
            type="button"
            onClick={onOpenSettings}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl transition-all text-xs font-medium border bg-slate-900 hover:bg-slate-800 text-slate-200 border-slate-800 hover:border-cyan-400/40 shadow-sm"
            title="Configuración de API Key y Parámetros"
          >
            <Settings className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden sm:inline">Ajustes</span>
          </button>

          {/* Button: Clear Chat (Reiniciar) */}
          <button
            type="button"
            onClick={onClearChat}
            className="p-2 rounded-xl transition-all border bg-slate-900 hover:bg-red-950/40 text-slate-400 hover:text-red-400 border-slate-800 shadow-sm"
            title="Reiniciar chat"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

      </div>
    </header>
  );
}
