$(function () {
    $(".download-zip").click(function(e) {
        e.preventDefault();
        downloadAsZip($(this)[0]);
        return false;
    })
})

function downloadAsZip (element) {
    var source = element.parentElement;

    // Search for parent element with class "download-zip-source"
    while (!source.classList.contains("download-zip-source")) {
        source = source.parentElement;
    }

    // Now find all image sources
    var srcs = [];
    var nodes = [source];
    while (nodes.length > 0) {
        var node = nodes.pop();
        if (node.tagName.toLowerCase() === "img") {
            srcs.push(node.src);
        }

        for (let i = 0; i < node.children.length; i++) {
            nodes.push(node.children[i]);
        }
    }

    // Zip the source files
    var zip = new JSZip();
    var count = 0;
    var zipFilename = element.getAttribute("file");

    srcs.forEach(function(url){
        var filename = url.substring(url.lastIndexOf('/')+1);
        // loading a file and add it in a zip file
        JSZipUtils.getBinaryContent(url, function (err, data) {
            if(err) {
                console.log(err);
                throw err; // or handle the error
            }
            zip.file(filename, data, {binary:true});
            count++;
            if (count == srcs.length) {
                zip.generateAsync({type:'blob'}).then(function(content) {
                    saveAs(content, zipFilename);
                });
            }
        });
    });
}