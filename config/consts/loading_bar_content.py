#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: loading_bar_content.py
#  Last Modified: 2024-10-05 15:31:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:25:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

CONTENT_MIX = '''
                <div id="loading-bar" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0, 0, 0, 0.5); z-index:9999; pointer-events:none;">
                    <img src="/static/img/loading/spinner-main.gif" alt="Loading..." style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); max-width:30%;" />
                </div>
                <script>
                    const loadingBar = document.getElementById("loading-bar");

                    // Show the loading bar when the page is navigating or fetching resources
                    window.addEventListener("beforeunload", function() {
                        loadingBar.style.display = "block";
                    });

                    // Hide the loading bar when the page is fully loaded
                    window.addEventListener("load", function() {
                        loadingBar.style.display = "none";
                    });

                    // Also listen to AJAX (fetch) requests if needed
                    (function() {
                        const originalFetch = window.fetch;

                        window.fetch = function(...args) {
                            loadingBar.style.display = "block";  // Show spinner on fetch request
                            return originalFetch(...args)
                                .then(response => {
                                    loadingBar.style.display = "none";  // Hide spinner on fetch completion
                                    return response;
                                })
                                .catch(error => {
                                    loadingBar.style.display = "none";  // Hide spinner on error
                                    throw error;
                                });
                        };
                    })();

                    // Hide the loading bar after DOM is fully loaded (for fast operations)
                    document.addEventListener("DOMContentLoaded", function() {
                        loadingBar.style.display = "none";
                    });
                </script>
            '''
