import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatContainer from './components/ChatContainer';
import SettingsModal from './components/SettingsModal';
import { sendQuery, getHealth, getCacheStats } from './services/api';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [health, setHealth] = useState(null);
  const [cacheStats, setCacheStats] = useState(null);
  
  // Permanent Dark Mode
  useEffect(() => {
    document.documentElement.classList.add('dark');
  }, []);

  // Modals state
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  
  // User Config (LocalStorage)
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('gemini_api_key') || '');
  const [similarityThreshold, setSimilarityThreshold] = useState(0.22);

  // Poll / Check backend health on mount
  useEffect(() => {
    fetchSystemStatus();
    const interval = setInterval(fetchSystemStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const [h, cs] = await Promise.all([
        getHealth().catch(() => null),
        getCacheStats().catch(() => null)
      ]);
      if (h) setHealth(h);
      if (cs) setCacheStats(cs);
    } catch (e) {
      console.warn("Backend poll warning:", e);
    }
  };

  const handleSendMessage = async (queryText) => {
    if (!queryText.trim() || loading) return;

    setError(null);
    const userMsg = {
      role: 'user',
      text: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const response = await sendQuery(queryText, apiKey);
      
      const assistantMsg = {
        role: 'assistant',
        answer: response.answer,
        is_escalated: response.is_escalated,
        escalation_reason: response.escalation_reason,
        ticket_id: response.ticket_id,
        confidence_score: response.confidence_score,
        citations: response.citations,
        latency_ms: response.latency_ms,
        from_cache: response.from_cache,
        model_used: response.model_used,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, assistantMsg]);
      fetchSystemStatus();
    } catch (err) {
      setError(`No fue posible procesar la consulta: ${err.message}. Asegúrate de que el backend esté en ejecución.`);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveApiKey = (newKey) => {
    setApiKey(newKey);
    if (newKey) {
      localStorage.setItem('gemini_api_key', newKey);
    } else {
      localStorage.removeItem('gemini_api_key');
    }
    fetchSystemStatus();
  };

  const handleClearChat = () => {
    if (messages.length === 0) return;
    if (window.confirm("¿Deseas reiniciar la conversación de chat con Poly?")) {
      setMessages([]);
      setError(null);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-dark-pattern text-slate-100 transition-colors duration-300">
      {/* Header */}
      <Header
        health={health}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onClearChat={handleClearChat}
      />

      {/* Main Chat Thread */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <ChatContainer
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
          error={error}
        />
      </main>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apiKey={apiKey}
        onSaveApiKey={handleSaveApiKey}
        similarityThreshold={similarityThreshold}
        onThresholdChange={(val) => setSimilarityThreshold(val)}
        cacheStats={cacheStats}
        onCacheCleared={fetchSystemStatus}
      />
    </div>
  );
}
