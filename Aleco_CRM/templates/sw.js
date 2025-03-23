self.addEventListener("install", (event) => {
  event.waitUntil(
      caches.keys().then((cacheNames) => {
          return Promise.all(cacheNames.map((cache) => caches.delete(cache))); // Delete all caches
      })
  );
  self.skipWaiting(); // Force activation immediately
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
      fetch(event.request).then((response) => {
          return response; // Always fetch fresh data
      }).catch(() => {
          return new Response("Network unavailable", { status: 503 });
      })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim()); // Ensure new service worker takes over
});
