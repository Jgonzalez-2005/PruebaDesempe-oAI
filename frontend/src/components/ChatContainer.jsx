import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, AlertCircle, Loader2, ShieldCheck, Headphones, Zap } from 'lucide-react';
import MessageBubble from './MessageBubble';
import SuggestionChips from './SuggestionChips';

export default function ChatContainer({ 
  messages, 
  onSendMessage, 
  loading, 
  error,
  theme 
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || loading) return;
    onSendMessage(inputText);
    setInputText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex-1 flex flex-col max-w-5xl w-full mx-auto px-4 sm:px-6 h-[calc(100vh-65px)]">
      
      {/* Scrollable Message List */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4 pr-1 sm:pr-2">
        
        {/* Welcome Hero when empty */}
        {messages.length === 0 && (
          <div className="my-6 sm:my-10 text-center max-w-3xl mx-auto space-y-5 animate-fadeIn">
            
            {/* Robot Poly Avatar Floating with Hover Zoom */}
            <div className="relative inline-block mx-auto group">
              <div className="w-32 h-28 sm:w-36 sm:h-32 mx-auto flex items-center justify-center cursor-pointer">
                <img 
                  src="/poly.png" 
                  alt="Robot Poly" 
                  className="w-full h-full object-contain filter drop-shadow-[0_12px_24px_rgba(6,182,212,0.30)] dark:drop-shadow-[0_12px_24px_rgba(6,182,212,0.45)] animate-float transition-all duration-300 ease-out hover:scale-125 hover:drop-shadow-[0_18px_36px_rgba(6,182,212,0.65)] cursor-pointer" 
                  title="¡Hola! Soy Poly"
                />
              </div>
              <div className="absolute top-0 right-1 bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md border border-white dark:border-slate-900 pointer-events-none">
                IA
              </div>
            </div>
            
            {/* High Contrast Central Greeting (Corporate Deep Blue & Charcoal in Light Mode) */}
            <div className="space-y-2.5">
              <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
                ¡Hola! Soy <span className="bg-gradient-to-r from-blue-700 via-sky-600 to-cyan-600 dark:from-cyan-400 dark:via-sky-300 dark:to-blue-400 bg-clip-text text-transparent font-extrabold">Poly</span>
              </h2>
              <p className="text-sm sm:text-base text-slate-700 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed font-normal">
                Tu asistente virtual oficial de LinguaColombia. Estoy aquí para <strong className="font-bold text-slate-950 dark:text-white">resolver tus dudas</strong> sobre programas de Inglés, Francés y Alemán, modalidades, horarios y certificaciones.
              </p>
            </div>

            {/* 3 Information Cards in Pure Brilliant White with Cyan Hover Lift Effect */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 text-left">
              
              {/* Card 1: Información Oficial */}
              <div className="card-hover-lift group p-5 rounded-2xl transition-all duration-300 bg-white dark:bg-[#0f172a] border border-slate-200 dark:border-slate-800 hover:border-cyan-400 dark:hover:border-cyan-400 shadow-md shadow-slate-200/80 dark:shadow-none hover:shadow-xl hover:shadow-cyan-500/15 dark:ring-1 dark:ring-white/5 cursor-default">
                <div className="w-10 h-10 rounded-xl bg-cyan-50 dark:bg-cyan-500/10 border border-cyan-200 dark:border-cyan-500/20 flex items-center justify-center text-cyan-600 dark:text-cyan-400 mb-3 group-hover:scale-110 group-hover:bg-cyan-500 group-hover:text-white transition-all duration-300 shadow-sm">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">
                  Información Oficial
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1.5 leading-relaxed font-normal">
                  Respuestas respaldadas directamente en los reglamentos y documentos oficiales de la academia.
                </p>
              </div>

              {/* Card 2: Atención Personalizada */}
              <div className="card-hover-lift group p-5 rounded-2xl transition-all duration-300 bg-white dark:bg-[#0f172a] border border-slate-200 dark:border-slate-800 hover:border-cyan-400 dark:hover:border-cyan-400 shadow-md shadow-slate-200/80 dark:shadow-none hover:shadow-xl hover:shadow-cyan-500/15 dark:ring-1 dark:ring-white/5 cursor-default">
                <div className="w-10 h-10 rounded-xl bg-sky-50 dark:bg-sky-500/10 border border-sky-200 dark:border-sky-500/20 flex items-center justify-center text-sky-600 dark:text-sky-400 mb-3 group-hover:scale-110 group-hover:bg-sky-500 group-hover:text-white transition-all duration-300 shadow-sm">
                  <Headphones className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-sky-600 dark:group-hover:text-sky-400 transition-colors">
                  Atención Personalizada
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1.5 leading-relaxed font-normal">
                  Transferencia directa a un asesor académico humano si requieres una orientación especial.
                </p>
              </div>

              {/* Card 3: Respuesta Rápida */}
              <div className="card-hover-lift group p-5 rounded-2xl transition-all duration-300 bg-white dark:bg-[#0f172a] border border-slate-200 dark:border-slate-800 hover:border-cyan-400 dark:hover:border-cyan-400 shadow-md shadow-slate-200/80 dark:shadow-none hover:shadow-xl hover:shadow-cyan-500/15 dark:ring-1 dark:ring-white/5 cursor-default">
                <div className="w-10 h-10 rounded-xl bg-cyan-50 dark:bg-cyan-500/10 border border-cyan-200 dark:border-cyan-500/20 flex items-center justify-center text-cyan-600 dark:text-cyan-400 mb-3 group-hover:scale-110 group-hover:bg-cyan-500 group-hover:text-white transition-all duration-300 shadow-sm">
                  <Zap className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">
                  Respuesta Inmediata
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1.5 leading-relaxed font-normal">
                  Atención en tiempo real las 24 horas para guiarte en tarifas, horarios y proceso de matrícula.
                </p>
              </div>

            </div>

          </div>
        )}

        {/* Conversation Bubbles */}
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}

        {/* Loading Bubble */}
        {loading && (
          <div className="flex items-center gap-3 my-4">
            <div className="w-8 h-8 flex items-center justify-center animate-pulse">
              <img 
                src="/poly.png" 
                alt="Poly" 
                className="w-full h-full object-contain filter drop-shadow-[0_2px_6px_rgba(6,182,212,0.4)] transition-transform duration-300 hover:scale-125 cursor-pointer" 
              />
            </div>
            <div className="p-3.5 rounded-2xl rounded-tl-sm bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs text-slate-800 dark:text-slate-200 flex items-center gap-2.5 shadow-md">
              <Loader2 className="w-4 h-4 animate-spin text-cyan-600 dark:text-cyan-400" />
              <span className="font-medium text-slate-700 dark:text-slate-300">Poly está consultando los documentos oficiales...</span>
            </div>
          </div>
        )}

        {/* Error Notification */}
        {error && (
          <div className="p-3.5 rounded-2xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800/50 text-red-800 dark:text-red-300 text-xs flex items-center gap-2.5 shadow-sm">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600" />
            <span className="font-medium">{error}</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Questions Accordion */}
      <div className="py-1">
        <SuggestionChips 
          onSelectQuery={(q) => onSendMessage(q)} 
          disabled={loading} 
        />
      </div>

      {/* Pure White Capsule Message Input Box with Vibrant Cyan Send Button */}
      <div className="py-3">
        <form 
          onSubmit={handleSubmit}
          className="relative flex items-center bg-white dark:bg-[#0f172a] border border-slate-300 dark:border-slate-800 focus-within:border-cyan-500 dark:focus-within:border-cyan-500 focus-within:ring-2 focus-within:ring-cyan-500/20 rounded-2xl p-1.5 shadow-lg shadow-slate-200/70 dark:shadow-2xl dark:shadow-black/50 transition-all duration-300"
        >
          <textarea
            ref={inputRef}
            rows={1}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Pregúntale a Poly sobre programas, precios, horarios o exámenes..."
            className="w-full bg-transparent px-4 py-2.5 text-xs sm:text-sm text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none resize-none max-h-32 min-h-[42px] font-normal"
          />

          <button
            type="submit"
            disabled={!inputText.trim() || loading}
            className={`p-2.5 rounded-xl transition-all duration-200 flex items-center justify-center flex-shrink-0 ${
              inputText.trim() && !loading
                ? 'bg-gradient-to-r from-cyan-500 via-sky-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-md shadow-cyan-500/30 hover:scale-105 active:scale-95'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed'
            }`}
            title="Enviar mensaje"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </form>
        <p className="text-[10px] text-center text-slate-500 dark:text-slate-400 mt-1.5 font-medium">
          Poly • Asistente Virtual LinguaColombia • Presiona <kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-[10px] font-mono">Enter</kbd> para enviar
        </p>
      </div>

    </div>
  );
}
