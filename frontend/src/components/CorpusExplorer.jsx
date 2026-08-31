import React, { useState, useEffect } from 'react';
import { X, Database, FileText, RefreshCw, Layers, Search } from 'lucide-react';
import { getDocuments, getChunks, reloadCorpus } from '../services/api';

export default function CorpusExplorer({ isOpen, onClose, onCorpusReloaded }) {
  const [documents, setDocuments] = useState([]);
  const [chunks, setChunks] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [searchChunkTerm, setSearchChunkTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [reloading, setReloading] = useState(false);
  const [activeTab, setActiveTab] = useState('docs');

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [docsData, chunksData] = await Promise.all([
        getDocuments(),
        getChunks()
      ]);
      setDocuments(docsData);
      setChunks(chunksData);
      if (docsData.length > 0 && !selectedDoc) {
        setSelectedDoc(docsData[0].filename);
      }
    } catch (err) {
      console.error("Error cargando documentos:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleReloadCorpus = async () => {
    try {
      setReloading(true);
      await reloadCorpus();
      await loadData();
      if (onCorpusReloaded) onCorpusReloaded();
    } catch (err) {
      alert("Error al actualizar documentos: " + err.message);
    } finally {
      setReloading(false);
    }
  };

  if (!isOpen) return null;

  const cleanDocTitle = (title) => {
    if (!title) return "Documento Oficial";
    return title.replace(/^\d+[\.\-_\s]*/, '').replace(' - LinguaColombia', '').trim();
  };

  const filteredChunks = chunks.filter(c => {
    const matchesDoc = selectedDoc ? c.doc_name === selectedDoc : true;
    const matchesSearch = searchChunkTerm 
      ? (c.text.toLowerCase().includes(searchChunkTerm.toLowerCase()) || c.section.toLowerCase().includes(searchChunkTerm.toLowerCase()))
      : true;
    return matchesDoc && matchesSearch;
  });

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm transition-all animate-fadeIn">
      <div className="w-full max-w-3xl h-full bg-white dark:bg-[#091322] border-l border-slate-200 dark:border-slate-800 flex flex-col shadow-2xl overflow-hidden transition-colors duration-300">
        
        {/* Header */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/80 dark:bg-slate-900/60">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-cyan-50 dark:bg-cyan-500/10 border border-cyan-200 dark:border-cyan-500/20 text-cyan-600 dark:text-cyan-400 shadow-sm">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">Documentos Oficiales del Negocio</h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Base de conocimiento oficial utilizada por Poly para responder
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleReloadCorpus}
              disabled={reloading}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 hover:bg-cyan-50 dark:hover:bg-slate-700 text-xs font-medium text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 transition-all disabled:opacity-50 shadow-sm"
              title="Actualizar documentos"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${reloading ? 'animate-spin text-cyan-500' : ''}`} />
              <span>{reloading ? 'Actualizando...' : 'Actualizar'}</span>
            </button>
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Tab Selector */}
        <div className="flex border-b border-slate-200 dark:border-slate-800 px-4 bg-slate-50/40 dark:bg-slate-900/40">
          <button
            type="button"
            onClick={() => setActiveTab('docs')}
            className={`flex items-center gap-2 py-3 px-4 text-xs font-semibold border-b-2 transition-colors ${
              activeTab === 'docs'
                ? 'border-cyan-500 text-cyan-600 dark:text-cyan-400'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Documentos ({documents.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('chunks')}
            className={`flex items-center gap-2 py-3 px-4 text-xs font-semibold border-b-2 transition-colors ${
              activeTab === 'chunks'
                ? 'border-cyan-500 text-cyan-600 dark:text-cyan-400'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Fragmentos de Información ({chunks.length})</span>
          </button>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {loading ? (
            <div className="h-64 flex flex-col items-center justify-center text-slate-400 gap-3">
              <RefreshCw className="w-8 h-8 animate-spin text-cyan-500" />
              <p className="text-xs">Cargando base de conocimiento...</p>
            </div>
          ) : activeTab === 'docs' ? (
            
            /* Vista de Documentos */
            <div className="space-y-3">
              {documents.map((doc, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-2xl bg-white dark:bg-[#0f172a]/70 border border-slate-200 dark:border-slate-800 hover:border-cyan-300 dark:hover:border-slate-700 transition-all shadow-sm space-y-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start gap-3">
                      <div className="p-2 rounded-xl bg-cyan-50 dark:bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 mt-0.5 shadow-sm">
                        <FileText className="w-4 h-4" />
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-slate-900 dark:text-white">{cleanDocTitle(doc.title)}</h3>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Reglamento Académico LinguaColombia</p>
                      </div>
                    </div>

                    <span className="inline-block px-2.5 py-1 rounded-full bg-cyan-50 dark:bg-cyan-500/10 text-cyan-700 dark:text-cyan-400 border border-cyan-200 dark:border-cyan-500/20 text-xs font-semibold">
                      {doc.chunk_count} secciones
                    </span>
                  </div>

                  {/* Secciones */}
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80">
                    <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
                      Temas incluidos:
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {doc.sections.map((sec, sIdx) => (
                        <span
                          key={sIdx}
                          className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 text-xs border border-slate-200 dark:border-slate-700 font-medium"
                        >
                          {sec.replace(/^\d+[\.\-_\s]*/, '')}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>

          ) : (

            /* Vista de Fragmentos */
            <div className="space-y-3">
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Buscar en los fragmentos de información..."
                  value={searchChunkTerm}
                  onChange={(e) => setSearchChunkTerm(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-900 dark:text-slate-200 placeholder:text-slate-400 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="space-y-2.5 max-h-[520px] overflow-y-auto pr-1">
                {filteredChunks.map((chunk, idx) => (
                  <div
                    key={idx}
                    className="p-3.5 rounded-2xl bg-white dark:bg-[#0f172a]/60 border border-slate-200 dark:border-slate-800/80 text-xs hover:border-cyan-300 dark:hover:border-slate-700 transition-all shadow-sm space-y-2"
                  >
                    <div className="font-semibold text-slate-900 dark:text-slate-200">
                      {chunk.section.replace(/^\d+[\.\-_\s]*/, '')}
                    </div>

                    <p className="text-slate-700 dark:text-slate-300 font-sans leading-relaxed bg-slate-50 dark:bg-slate-950/80 p-3 rounded-xl border border-slate-100 dark:border-slate-800/50 whitespace-pre-wrap text-[11.5px]">
                      {chunk.text}
                    </p>
                  </div>
                ))}
              </div>

            </div>
          )}

        </div>

      </div>
    </div>
  );
}
