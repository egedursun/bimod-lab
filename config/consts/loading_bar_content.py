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
