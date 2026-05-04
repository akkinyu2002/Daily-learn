import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';

console.log('[Main] App starting...');

const rootElement = document.getElementById('root');

if (!rootElement) {
  console.error('[Main] Root element not found! Check index.html');
  document.body.innerHTML = '<div style="color: red; padding: 20px;">ERROR: Root element (#root) not found in HTML</div>';
  throw new Error('Root element not found');
}

console.log('[Main] Root element found, mounting React app...');

try {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
  console.log('[Main] React app mounted successfully');
} catch (error) {
  console.error('[Main] Failed to mount React app:', error);
  rootElement.innerHTML = `
    <div style="color: red; padding: 20px; font-family: monospace;">
      <h2>Failed to mount React app</h2>
      <pre>${error}</pre>
    </div>
  `;
}
