/*
 * Transitional cleanup worker.
 *
 * The site no longer registers a service worker: the previous implementation
 * only added NetworkFirst image caching and did not provide a coherent offline
 * experience. Existing registrations will update to this worker, remove their
 * Workbox runtime caches, and unregister themselves.
 */
self.addEventListener('install', function () {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(
          keys
            .filter(function (key) { return key.indexOf('workbox-') === 0; })
            .map(function (key) { return caches.delete(key); })
        );
      })
      .then(function () { return self.registration.unregister(); })
  );
});
