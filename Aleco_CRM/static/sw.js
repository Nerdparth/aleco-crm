self.addEventListener("install", (event) => {
    event.waitUntil(
      caches.open("django-pwa").then((cache) => {
        return cache.addAll([
          "/",
          "/static/pwa/image.png", // Icons
        ]);
      })
    );
  });
  
  self.addEventListener("fetch", (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });
  