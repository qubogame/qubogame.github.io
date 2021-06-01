(function() {
    // Do not run in local mode
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.hostname === "")
        return;

    var langs = {"es": "/lang/es/", "fr": "/lang/fr/"};

    var scriptTag = document.currentScript;
    var page = scriptTag.getAttribute("page");
    var language = navigator.language.split('-')[0];

    if (langs.hasOwnProperty(language)) {
        // The desired language is supported, redirect to it
        var redirect = langs[language] + page;
        window.location.replace(redirect);
    }
})();