import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Headphones, 
  User, 
  Copy, 
  Check, 
  Ticket, 
  Clock, 
  Zap, 
  Sparkles 
} from 'lucide-react';
import EvidenceViewer from './EvidenceViewer';

export default function MessageBubble({ message }) {
  const [copied, setCopied] = useState(false);
  const [showEvidence, setShowEvidence] = useState(false);

  const isUser = message.role === 'user';
  const isEscalated = message.is_escalated;

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text || message.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderFormattedText = (text) => {
    if (!text) return null;
    
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
        const content = line.trim().substring(1).trim();
        return (
          <div key={idx} className="flex items-start gap-2 my-1 pl-1">
            <span className="text-cyan-600 dark:text-cyan-400 mt-1 flex-shrink-0 text-xs">•</span>
            <span className="leading-relaxed" dangerouslySetInnerHTML={{ __html: formatBold(content) }} />
          </div>
        );
      }
      
      const numMatch = line.trim().match(/^(\d+)\.\s*(.*)$/);
      if (numMatch) {
        return (
          <div key={idx} className="flex items-start gap-2 my-1 pl-1">
            <span className="text-cyan-600 dark:text-cyan-400 font-semibold font-mono text-xs flex-shrink-0">{numMatch[1]}.</span>
            <span className="leading-relaxed" dangerouslySetInnerHTML={{ __html: formatBold(numMatch[2]) }} />
          </div>
        );
      }

      if (!line.trim()) {
        return <div key={idx} className="h-2" />;
      }

      return (
        <p key={idx} className="my-1 leading-relaxed" dangerouslySetInnerHTML={{ __html: formatBold(line) }} />
      );
    });
  };

  const formatBold = (str) => {
    return str.replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-950 dark:text-white font-semibold">$1</strong>');
  };

  if (isUser) {
    return (
      <div className="flex justify-end gap-3 my-4">
        <div className="max-w-2xl bg-gradient-to-r from-blue-700 via-sky-600 to-cyan-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 shadow-md shadow-blue-950/10">
          <p className="text-sm leading-relaxed font-medium">{message.text}</p>
          <div className="text-[10px] text-cyan-100/90 text-right mt-1 font-mono">
            {message.timestamp || 'Ahora'}
          </div>
        </div>
        <div className="w-8 h-8 rounded-xl bg-blue-700 text-white flex items-center justify-center flex-shrink-0 shadow-sm">
          <User className="w-4 h-4" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start gap-3 my-4">
      <div className={`w-8 h-8 flex items-center justify-center flex-shrink-0 ${
        isEscalated 
          ? 'rounded-xl bg-amber-100 dark:bg-amber-600/30 border border-amber-300 dark:border-amber-500/60 text-amber-700 dark:text-amber-300 p-1.5 shadow-sm' 
          : 'p-0.5'
      }`}>
        {isEscalated ? (
          <Headphones className="w-full h-full" />
        ) : (
          <img 
            src="/poly.png" 
            alt="Poly" 
            className="w-full h-full object-contain filter drop-shadow-[0_2px_6px_rgba(6,182,212,0.35)] transition-all duration-300 ease-out hover:scale-150 hover:z-20 hover:drop-shadow-[0_4px_12px_rgba(6,182,212,0.7)] cursor-pointer" 
            title="Poly"
          />
        )}
      </div>

      <div className={`max-w-3xl w-full rounded-2xl rounded-tl-sm p-4 text-slate-800 dark:text-slate-200 shadow-md dark:shadow-xl backdrop-blur-sm border transition-all duration-300 ${
        isEscalated 
          ? 'bg-amber-50/70 dark:bg-amber-950/20 border-amber-200 dark:border-amber-500/30 ring-1 ring-amber-400/20' 
          : 'bg-white dark:bg-[#0f172a] border-slate-200/90 dark:border-slate-800 ring-1 ring-slate-100 dark:ring-white/5'
      }`}>
        
        {/* Top bar */}
        <div className="flex items-center justify-between gap-2 pb-2.5 mb-2.5 border-b border-slate-100 dark:border-slate-800/80">
          <div className="flex items-center gap-2">
            {isEscalated ? (
              <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-800 dark:text-amber-300 bg-amber-100/80 dark:bg-amber-500/10 px-2.5 py-1 rounded-lg border border-amber-300 dark:border-amber-500/30">
                <Headphones className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                <span>Atención con Asesor Académico</span>
              </div>
            ) : (
              <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-900 dark:text-cyan-300 bg-cyan-50 dark:bg-cyan-500/10 px-2.5 py-1 rounded-lg border border-cyan-200 dark:border-cyan-500/30">
                <ShieldCheck className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" />
                <span>Poly • Asistente Oficial</span>
              </div>
            )}

            {message.ticket_id && (
              <span className="flex items-center gap-1 text-[11px] font-mono font-semibold px-2 py-0.5 rounded-md bg-amber-100 dark:bg-amber-500/20 text-amber-800 dark:text-amber-200 border border-amber-300 dark:border-amber-400/30">
                <Ticket className="w-3 h-3 text-amber-600 dark:text-amber-300" />
                {message.ticket_id}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleCopy}
              className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
              title="Copiar respuesta"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        {/* Message body */}
        <div className="text-xs sm:text-sm font-normal text-slate-800 dark:text-slate-200 leading-relaxed">
          {renderFormattedText(message.answer || message.text)}
        </div>

        {/* Evidence viewer */}
        {message.citations && message.citations.length > 0 && !isEscalated && (
          <EvidenceViewer 
            citations={message.citations} 
            isOpen={showEvidence} 
            onToggle={() => setShowEvidence(!showEvidence)} 
          />
        )}

        {/* Bottom meta bar */}
        <div className="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/60 flex flex-wrap items-center justify-between gap-2 text-[10px] text-slate-500 dark:text-slate-400 font-mono">
          <div className="flex items-center gap-3">
            {message.latency_ms !== undefined && (
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3 text-slate-400" />
                {message.latency_ms} ms
              </span>
            )}

            {message.from_cache && (
              <span className="flex items-center gap-1 text-cyan-700 dark:text-cyan-400 font-semibold bg-cyan-50 dark:bg-cyan-500/10 px-1.5 py-0.5 rounded border border-cyan-200 dark:border-cyan-500/20">
                <Zap className="w-3 h-3" />
                Instantáneo (Caché)
              </span>
            )}
          </div>

          <div className="flex items-center gap-1 text-slate-500 dark:text-slate-400">
            <Sparkles className="w-3 h-3 text-cyan-600 dark:text-cyan-400" />
            <span>Poly AI • LinguaColombia</span>
          </div>
        </div>

      </div>
    </div>
  );
}
