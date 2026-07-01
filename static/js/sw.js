// Basic Service Worker for PWA support
const CACHE_NAME = 'amotekun-v1';
const urlsToCache = [
    '/',
    '/static/css/output.css',
    '/static/css/style.css',
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});