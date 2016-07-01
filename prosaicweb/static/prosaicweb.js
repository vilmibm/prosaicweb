// prosaicweb.js
// shared javascript for prosaicweb

(function () {
    window.prosaicweb = {};

    // this is a pretty dumb hack.
    JSON.pretty_print = function (json_string) {
        return this.stringify(this.parse(json_string), undefined, 2);
    };

    // fuck you javascript
    NodeList.prototype.forEach = Array.prototype.forEach;

    prosaicweb.prettify_textareas = function() {
        document.querySelectorAll("textarea.json").forEach(
            function(ta) {
                ta.value = JSON.pretty_print(ta.value);
            }
        );
    };

    window.addEventListener('load', prosaicweb.prettify_textareas);

})();
