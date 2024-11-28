/*
 * Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
 *
 * Project: Bimod.io™
 * File: service-worker.js
 * Last Modified: 2024-11-27 23:34:21
 * Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
 * Created: 2024-11-27 23:34:22
 *
 * This software is proprietary and confidential. Unauthorized copying,
 * distribution, modification, or use of this software, whether for
 * commercial, academic, or any other purpose, is strictly prohibited
 * without the prior express written permission of BMD™ Autonomous
 * Holdings.
 *
 *  For permission inquiries, please contact: admin@Bimod.io.
 *
 */

self.addEventListener('install', (event) => {
    console.log('Service Worker: Install event triggered.');
    // Skip the waiting phase and immediately activate the service worker
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activate event triggered.');
    console.log('Service Worker: Now ready to handle fetch events.');
    // Ensure the service worker takes control of the page immediately
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    console.log('Service Worker: Fetch event triggered for URL:', event.request.url);

    // Fetch requests without any caching
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                console.log('Service Worker: Successfully fetched:', event.request.url);
                return response;
            })
            .catch((error) => {
                console.error('Service Worker: Fetch failed for URL:', event.request.url, 'Error:', error);
                throw error; // Rethrow the error to ensure it's visible
            })
    );
});

