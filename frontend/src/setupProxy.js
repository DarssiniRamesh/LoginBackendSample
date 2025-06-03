const { createProxyMiddleware } = require('http-proxy-middleware');

/**
 * Proxy any request with /api/* to the Flask backend at localhost:5000 during development.
 * This avoids CORS errors and lets you use absolute fetch('/api/...') in your code.
 */
module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
    })
  );
};
