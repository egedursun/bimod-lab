CONTENT_MIX = '''
    <div id="loading-bar" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0, 0, 0, 0.5); z-index:9999; pointer-events:auto;">
        <img id="spinner-image" src="/static/img/loading/spinner-main.gif" alt="Loading..." style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); max-width:30%;" />
    </div>
    <script>
        (function() {
            const originalFetch = window.fetch;
            const loadingBar = document.getElementById("loading-bar");
            const spinnerImage = document.getElementById("spinner-image");

            // Intercept fetch calls with delay to prevent first-click issues
            window.fetch = function(...args) {
                setTimeout(() => {
                    loadingBar.style.display = "block";  // Show spinner after a small delay
                    loadingBar.style.pointerEvents = "auto";  // Enable blocking clicks
                }, 100);  // Adjust delay to ensure smooth handling of clicks

                return originalFetch(...args)
                    .then(response => {
                        loadingBar.style.display = "none";  // Hide spinner
                        loadingBar.style.pointerEvents = "none";  // Allow clicks again
                        return response;
                    })
                    .catch(error => {
                        loadingBar.style.display = "none";  // Hide spinner on error
                        loadingBar.style.pointerEvents = "none";  // Allow clicks again
                        throw error;
                    });
            };

            // Allow user to hide loading bar by clicking outside the spinner image
            loadingBar.addEventListener('click', function(event) {
                if (event.target !== spinnerImage) {
                    loadingBar.style.display = "none";  // Hide the loading bar
                }
            });
        })();
    </script>
'''
