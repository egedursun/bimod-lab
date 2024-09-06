CONTENT_MIX = '''
                <div id="loading-bar" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0, 0, 0, 0.5); z-index:9999; pointer-events:none;">
                    <img src="/static/img/loading/spinner-main.gif" alt="Loading..." style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); max-width:30%;" />
                </div>
                <script>
                    (function() {
                        const originalFetch = window.fetch;

                        // Intercepting fetch calls with delay to prevent first-click issues
                        window.fetch = function(...args) {
                            setTimeout(() => {
                                document.getElementById("loading-bar").style.display = "block";  // Show spinner after a small delay
                                document.getElementById("loading-bar").style.pointerEvents = "auto";  // Enable blocking clicks
                            }, 100);  // Adjust delay to ensure smooth handling of clicks

                            return originalFetch(...args)
                                .then(response => {
                                    document.getElementById("loading-bar").style.display = "none";  // Hide spinner
                                    document.getElementById("loading-bar").style.pointerEvents = "none";  // Allow clicks again
                                    return response;
                                })
                                .catch(error => {
                                    document.getElementById("loading-bar").style.display = "none";  // Hide spinner on error
                                    document.getElementById("loading-bar").style.pointerEvents = "none";  // Allow clicks again
                                    throw error;
                                });
                        };
                    })();
                </script>
            '''
