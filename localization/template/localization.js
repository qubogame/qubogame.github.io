(function() {
    var langs = {{LANG}};

    var scriptTag = document.currentScript;
    var page = scriptTag.getAttribute("page");
    var language = navigator.language.split('-')[0];
    
    if (langs.hasOwnProperty(language)) {
        // The desired language is supported, redirect to it
        var redirect = langs[language] + page;
        window.location.replace(redirect);
    }
})();