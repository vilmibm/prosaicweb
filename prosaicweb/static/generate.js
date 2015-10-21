// generate.js
// code for the poetry generation form
console.log('loaded generate.js');
(function () {
    var template_select = document.querySelector('#templates');
    var template_textarea = document.querySelector('textarea');
    var form = document.querySelector('form');
    var output = document.querySelector('#output');
    var preselected_template_option = template_select.selectedOptions[0];

    template_textarea.update = function (new_content) {
        // content is going to be a json string. we do a dumb hack here to get
        // it pretty-printed:
        this.innerHTML = JSON.stringify(JSON.parse(new_content), undefined, 2);
    }

    // events
    var template_selected = function (e) {
        var option = e.explicitOriginalTarget;
        template_textarea.update(option.dataset.content);
    };

    var successful_generation = function (e) {
        var lines = JSON.parse(e.target.response).result;
        var pre = document.createElement('pre');
        pre.innerHTML = lines.join("\n");
        var existing_poems = output.querySelectorAll('pre');
        if (existing_poems.length == 0) {
            output.appendChild(pre);
        }
        else {
            output.insertBefore(pre, existing_poems[0]);
        }
    };

    var submit_generation = function (e) {
        e.preventDefault();

        var form_data = new FormData(form);
        var request = new XMLHttpRequest();

        request.open("POST", "/generate");
        request.send(form_data);
        request.addEventListener('load', successful_generation);
    };

    // helpers

    // init
    template_select.addEventListener('change', template_selected);
    form.addEventListener('submit', submit_generation, true);

    template_textarea.update(preselected_template_option.dataset.content);
})();
