/*
 * Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
 *
 * Project: Bimod.io™
 * File: service-worker.js
 * Last Modified: 2024-11-28 01:11:26
 * Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
 * Created: 2024-11-28 20:20:58
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
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activate event triggered.');
    console.log('Service Worker: Now ready to handle fetch events.');
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    console.log('Service Worker: Fetch event triggered for URL:', event.request.url);
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                console.log('Service Worker: Successfully fetched:', event.request.url);
                return response;
            })
            .catch((error) => {
                console.error('Service Worker: Fetch failed for URL:', event.request.url, 'Error:', error);
                throw error;
            })
    );
});

