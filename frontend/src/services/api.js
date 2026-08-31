const API_BASE = import.meta.env.VITE_API_BASE || import.meta.env.VITE_API_BASE_URL || '/api';

export async function sendQuery(query, apiKey = null, useCache = true) {
  const payload = {
    query: query.trim(),
    use_cache: useCache,
  };
  if (apiKey && apiKey.trim()) {
    payload.api_key = apiKey.trim();
  }

  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Error de conexión con el servidor' }));
    throw new Error(errorData.detail || `Error HTTP ${response.status}`);
  }

  return await response.json();
}

export async function getDocuments() {
  const response = await fetch(`${API_BASE}/documents`);
  if (!response.ok) throw new Error('Error al cargar documentos');
  return await response.json();
}

export async function getChunks(docName = null) {
  const url = docName ? `${API_BASE}/chunks?doc_name=${encodeURIComponent(docName)}` : `${API_BASE}/chunks`;
  const response = await fetch(url);
  if (!response.ok) throw new Error('Error al cargar chunks');
  return await response.json();
}

export async function reloadCorpus() {
  const response = await fetch(`${API_BASE}/reload-corpus`, { method: 'POST' });
  if (!response.ok) throw new Error('Error al recargar corpus');
  return await response.json();
}

export async function getCacheStats() {
  const response = await fetch(`${API_BASE}/cache/stats`);
  if (!response.ok) throw new Error('Error al obtener estadísticas de caché');
  return await response.json();
}

export async function clearCache() {
  const response = await fetch(`${API_BASE}/cache/clear`, { method: 'POST' });
  if (!response.ok) throw new Error('Error al limpiar caché');
  return await response.json();
}

export async function updateConfig(config) {
  const response = await fetch(`${API_BASE}/config`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  });
  if (!response.ok) throw new Error('Error al actualizar configuración');
  return await response.json();
}

export async function getHealth() {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) throw new Error('Servidor no disponible');
  return await response.json();
}
