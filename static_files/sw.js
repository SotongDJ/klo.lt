// reference: https://github.com/mdn/sw-test
const currentVersion = 'v01r038';
const addResourcesToCache = async (resources) => {
    const cache = await caches.open(currentVersion);
    await cache.addAll(resources);
};
const putInCache = async (request, response) => {
    const cache = await caches.open(currentVersion);
    await cache.put(request, response);
};
const cacheFirst = async ({ request, preloadResponsePromise, fallbackUrl }) => {
    // First try to get the resource from the cache
    const responseFromCache = await caches.match(request);
    if (responseFromCache) {return responseFromCache;};
    // Next try to use the preloaded response, if it's there
    const preloadResponse = await preloadResponsePromise;
    if (preloadResponse) {
        console.info('using preload response', preloadResponse);
        putInCache(request, preloadResponse.clone());
        return preloadResponse;
    };
    // Next try to get the resource from the network
    try {
        const responseFromNetwork = await fetch(request);
        // response may be used only once
        // we need to save clone to put one copy in cache
        // and serve second one
        putInCache(request, responseFromNetwork.clone());
        return responseFromNetwork;
    } catch (error) {
        const fallbackResponse = await caches.match(fallbackUrl);
        if (fallbackResponse) {return fallbackResponse;};
        // when even the fallback response is not available,
        // there is nothing we can do, but we must always
        // return a Response object
        return new Response('Network error happened', {
            status: 408,
            headers: { 'Content-Type': 'text/plain' }
        });
    };
};
// Enable navigation preloads!
const enableNavigationPreload = async () => {
    if (self.registration.navigationPreload) {await self.registration.navigationPreload.enable();};
};
const deleteCache = async (key) => {await caches.delete(key);};
const deleteOldCaches = async () => {
    const cacheKeepList = [currentVersion];
    const keyList = await caches.keys();
    const cachesToDelete = keyList.filter((key) => !cacheKeepList.includes(key));
    await Promise.all(cachesToDelete.map(deleteCache));
};
precache_arr = [
    '/',
    '/index.html',
    '/link.js?v01r038',
    '/main.css?v01r038',
    '/main.js?v01r038',
    '/clock.js?v01r038',
    '/extra.js?v01r038',
    '/site.js?v01r038',
    '/f/icon.css?v01r038',
    '/f/font.css?v01r038',
    '/podcast/main.css?v01r038',
    '/podcast/main.js?v01r038',
];
self.addEventListener('activate', (event) => {
    event.waitUntil(enableNavigationPreload());
    event.waitUntil(deleteOldCaches());
});
self.addEventListener('install', (event) => {event.waitUntil(addResourcesToCache(precache_arr));});
self.addEventListener('fetch', (event) => {
    event.respondWith(
        cacheFirst({
            request: event.request,
            preloadResponsePromise: event.preloadResponse,
            fallbackUrl: ''
        })
    );
});
