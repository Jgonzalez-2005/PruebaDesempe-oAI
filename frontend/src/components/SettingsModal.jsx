import React, { useState, useEffect } from 'react';
import { X, Key, Sliders, Zap, Shield, Save, CheckCircle2, Trash2 } from 'lucide-react';
import { updateConfig, clearCache } from '../services/api';

export default function SettingsModal({ 
  isOpen, 
  onClose, 
  apiKey, 
  onSaveApiKey, 
  similarityThreshold, 
  onThresholdChange,
  cacheStats,
  onCacheCleared
}) {
  const [keyInput, setKeyInput] = useState(apiKey || '');
  const [threshold, setThreshold] = useState(similarityThreshold || 0.08);
  const [model, setModel] = useState('gemini-2.5-flash');
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [clearingCache, setClearingCache] = useState(false);

  useEffect(() => {
    setKeyInput(apiKey || '');
    setThreshold(similarityThreshold || 0.08);
  }, [apiKey, similarityThreshold, isOpen]);

  if (!isOpen) return null;

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await updateConfig({
        gemini_api_key: keyInput.trim() || null,
        confidence_threshold: parseFloat(threshold),
        gemini_model: model
      });
      onSaveApiKey(keyInput.trim());
      onThresholdChange(parseFloat(threshold));
      setSavedSuccess(true);
      setTimeout(() => {
        setSavedSuccess(false);
        onClose();
      }, 1200);
    } catch (err) {
      alert("Error al guardar configuración: " + err.message);
    }
  };

  const handleClearCache = async () => {
    try {
      setClearingCache(true);
      await clearCache();
      if (onCacheCleared) onCacheCleared();
    } catch (err) {
      alert("Error limpiando caché: " + err.message);
    } finally {
      setClearingCache(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-lg bg-white dark:bg-[#091322] border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl overflow-hidden transition-colors duration-300">
        
        {/* Header */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/80 dark:bg-slate-900/60">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-cyan-50 dark:bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 shadow-sm">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">Ajustes del Asistente Poly</h3>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">Configuración de modelos y memoria</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSave} className="p-5 space-y-4">
          
          {/* API Key */}
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
              <Key className="w-3.5 h-3.5 text-cyan-600 dark:text-cyan-400" />
              API Key (OpenAI o Google Gemini - Opcional)
            </label>
            <input
              type="password"
              placeholder="sk-... o AIzaSy..."
              value={keyInput}
              onChange={(e) => setKeyInput(e.target.value)}
              className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl px-3.5 py-2 text-xs font-mono text-slate-900 dark:text-slate-200 placeholder:text-slate-400 dark:placeholder:text-slate-600 focus:outline-none focus:border-cyan-500"
            />
            <p className="text-[11px] text-slate-500 dark:text-slate-400">
              Si no configuras una API Key, Poly responderá en modo local determinista sin costo.
            </p>
          </div>

          {/* Similarity Threshold */}
          <div className="space-y-1.5 pt-2 border-t border-slate-100 dark:border-slate-800/80">
            <div className="flex justify-between items-center text-xs">
              <label className="font-semibold text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5 text-cyan-600" />
                Sensibilidad de Escalamiento a Asesor Humano
              </label>
              <span className="font-mono text-cyan-600 dark:text-cyan-400 font-bold">{threshold}</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.30"
              step="0.01"
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              className="w-full accent-cyan-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-500 dark:text-slate-400">
              <span>Más permisivo (0.05)</span>
              <span>Recomendado (0.08)</span>
              <span>Más estricto (0.30)</span>
            </div>
          </div>

          {/* Cache Management */}
          <div className="p-3 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-800 dark:text-slate-200">
                <Zap className="w-3.5 h-3.5 text-cyan-600" />
                <span>Memoria Caché de Respuestas Rápidas</span>
              </div>
              <button
                type="button"
                onClick={handleClearCache}
                disabled={clearingCache}
                className="flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-lg bg-white dark:bg-slate-800 hover:bg-red-50 dark:hover:bg-red-950 text-slate-700 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-300 border border-slate-200 dark:border-slate-700 transition-colors shadow-sm"
              >
                <Trash2 className="w-3 h-3" />
                <span>{clearingCache ? 'Vaciando...' : 'Vaciar Caché'}</span>
              </button>
            </div>
            
            {cacheStats && (
              <div className="grid grid-cols-3 gap-2 text-[11px] font-mono text-slate-500 dark:text-slate-400 pt-1">
                <div>Hits: <span className="text-cyan-600 dark:text-cyan-400 font-semibold">{cacheStats.hits}</span></div>
                <div>Misses: <span className="text-slate-700 dark:text-slate-300">{cacheStats.misses}</span></div>
                <div>Elementos: <span className="text-slate-700 dark:text-slate-300">{cacheStats.size}</span></div>
              </div>
            )}
          </div>

          {/* Buttons */}
          <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-semibold shadow-md shadow-cyan-900/20 transition-all"
            >
              {savedSuccess ? (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>¡Guardado!</span>
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  <span>Guardar Ajustes</span>
                </>
              )}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
}
