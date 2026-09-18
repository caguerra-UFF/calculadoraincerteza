/* Service Worker - Calculadora de Incerteza ISO/IEC 17025
   Cache local para funcionamento 100% offline em bancadas e laboratórios */

const CACHE_NAME = 'incerteza-iso17025-v4.6';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon.svg',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './assets/logo_eletronuclear.png',
  './assets/logo_elma.png',
  './assets/logo_ien.png',
  './assets/logo_uerj.png',
  './assets/logo_uff.png',
  './assets/icons/file-input.svg',
  './assets/icons/file-output.svg',
  './assets/icons/file-plus.svg',
  './assets/icons/file-text.svg',
  './assets/icons/file-up.svg',
  './assets/icons/graduation-cap.svg',
  './assets/icons/book-open-text.svg',
  './assets/icons/moon.svg',
  './assets/icons/expand.svg',
  './assets/icons/repeat.svg',
  './assets/icons/scale.svg',
  './assets/icons/sigma.svg',
  './assets/icons/square-sigma.svg',
  './assets/icons/circle-check.svg',
  './assets/icons/percent.svg',
  './assets/icons/percent-circle.svg',
  './assets/icons/waves.svg',
  './assets/icons/boxes.svg',
  './guia_calculadora/vendor/pdfjs/pdf.min.js',
  './guia_calculadora/vendor/pdfjs/pdf.worker.min.js',
  './docs/Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });
        return response;
      }).catch(() => {
        // Fallback para index.html se for navegação
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
